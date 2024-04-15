from typing import Literal

from pydantic import BaseModel


class Team(BaseModel):
    name: str
    description: str
    members: list[str]


class ActionsVar(BaseModel):
    name: str
    value: str


class Actions(BaseModel):
    enabled: bool = True
    variables: list[ActionsVar] = []
    secrets: list[ActionsVar] = []


class RepositoryTeam(BaseModel):
    name: str
    permission: Literal["pull", "triage", "push"]


class Repository(BaseModel):
    name: str
    description: str
    topics: list[str] = []
    teams: list[RepositoryTeam]
    actions: Actions = Actions()


class GitHubConfig(BaseModel):
    teams: list[Team]
    repositories: list[Repository]
