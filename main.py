"""Push a badge in response to a build event"""
import base64
import json
import os
from string import Template

from pydantic.error_wrappers import ValidationError
import google.cloud
from google.cloud import storage

from cloud_build_badge.cloud_build_message import CloudBuildMessage, RepoSource

BRANCH_TEMPLATE = "builds/{repo}/branches/{branch}.svg"
TAG_TEMPLATE = "builds/{repo}.svg"


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
    branch_template = os.environ.get("BRANCH_TEMPLATE_PATH", BRANCH_TEMPLATE)
    tag_template = os.environ.get("TAG_TEMPLATE_PATH", TAG_TEMPLATE)
    bucket = os.environ["BADGES_BUCKET"]

    decoded = base64.b64decode(event["data"]).decode("utf-8")
    try:
        message = CloudBuildMessage.parse_raw(decoded)
    except ValidationError as exception:
        print(decoded)
        raise exception

    src = f"badges/{message.status.lower()}.svg"
    if message.substitutions:
        if message.substitutions.BRANCH_NAME:
            dest = branch_template.format(
                repo=message.substitutions.REPO_NAME,
                branch=message.substitutions.BRANCH_NAME,
            )
        elif message.substitutions.TAG_NAME:
            dest = tag_template.format(repo=message.substitutions.REPO_NAME)
        else:
            raise NotImplementedError(f"message has no branch or tag: {message}")
    elif isinstance(message.source, RepoSource):
        dest = branch_template.format(
            repo=message.source.repoSource.repoName,
            branch=message.source.repoSource.branchName,
        )
    else:
        raise NotImplementedError(f"no repo: {message}")

    copy_badge(bucket, src, dest)
