"""Push a badge in response to a build event"""
import base64
import os

import google.cloud
from google.cloud import storage

from cloud_build_badge.cloud_build_message import CloudBuildMessage, RepoSource

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
    message = CloudBuildMessage.parse_raw(decoded)

    if isinstance(message.source, RepoSource):
        src = f"badges/{message.status.lower()}.svg"
        dest = template.format(
            repo=message.source.repoSource.repoName,
            branch=message.source.repoSource.branchName,
        )
        copy_badge(bucket, src, dest)
