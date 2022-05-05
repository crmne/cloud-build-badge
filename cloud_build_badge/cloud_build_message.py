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

    class Config:
        fields = {
            'object_': 'object'
        }


class StorageSource(BaseModel):
    storageSource: StorageSourceImpl


class StorageSourceManifest(BaseModel):
    storageSourceManifest: StorageSourceImpl

class Substitutions(BaseModel):
    REPO_NAME: str
    BRANCH_NAME: Optional[str]
    TAG_NAME: Optional[str]

class EmptySource(BaseModel):
    ...


class CloudBuildMessage(BaseModel):
    status: str
    source: Optional[Union[RepoSource, StorageSource, StorageSourceManifest, EmptySource]]
    substitutions: Optional[Substitutions]
