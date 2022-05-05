"""Push a badge in response to a build event"""
import base64
import json
import os
from string import Template

import google.cloud
from google.cloud import storage

DEFAULT_TEMPLATE = "builds/{repo}/branches/{branch}.svg"


def copy_badge(bucket, obj, new_obj):
    """Copy a badge to a public cloud storage bucket."""
    client = storage.Client()

    try:
        bucket = client.get_bucket(bucket)
    except google.cloud.exceptions.NotFound as ex:
        raise RuntimeError(f"Could not find bucket {bucket}") from ex

    blob = bucket.get_blob(obj)
    if blob is None:
        raise RuntimeError(f"Couldn't find object {obj} in bucket {bucket}")

    bucket.copy_blob(blob, bucket, new_name=new_obj)


def build_badge(event, context) -> None:
    """Create an push a badge in response to a build event."""
    template = os.environ.get("TEMPLATE_PATH", DEFAULT_TEMPLATE)
    bucket = os.environ["BADGES_BUCKET"]

    decoded = base64.b64decode(event["data"]).decode("utf-8")
    data = json.loads(decoded)

    status = data["status"]
    if "substitutions" in data:
        substitutions = data["substitutions"]
        if "REPO_NAME" in substitutions:
            repo = substitutions["REPO_NAME"]
            branch = substitutions["BRANCH_NAME"]
        else:
            raise NotImplementedError(f"input not recognized: {data}")
    elif "source" in data:
        repo_source = data["source"]["repoSource"]
        repo = repo_source["repoName"]
        branch = repo_source["branchName"]
    else:
        raise NotImplementedError(f"input not recognized: {data}")

    src = f"badges/{status.lower()}.svg"
    dest = template.format(repo=repo, branch=branch)
    copy_badge(bucket, src, dest)
