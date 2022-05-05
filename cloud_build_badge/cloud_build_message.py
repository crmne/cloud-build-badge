from re import S
from typing import Union, Optional
from pydantic import BaseModel


class RepoSourceImpl(BaseModel):
    projectId: Optional[str]
    repoName: str
    branchName: str
    tagName: Optional[str]


class RepoSource(BaseModel):
    repoSource: RepoSourceImpl


class StorageSourceImpl(BaseModel):
    bucket: str
    object_: str
    generation: Optional[int]


class StorageSource(BaseModel):
    storageSource: StorageSourceImpl


class StorageSourceManifest(BaseModel):
    storageSourceManifest: StorageSourceImpl


class CloudBuildMessage(BaseModel):
    status: str
    source: Union[RepoSource, StorageSource, StorageSourceManifest]
