from dataclasses import dataclass
from enum import Enum


INTRA_JSON_FILE = "intra/server/groups.json"
MY_RESULTS_PATH = "my/results"

FINAL_RESULT = "groups.json"


class Status(Enum):
    NOT_ACCEPTED = 0
    ACCEPTED = 1


@dataclass
class Member:
    login: str
    full_name: str
    status: Status


@dataclass
class Group:
    name: str
    members: list[Member]
    leader_login: str


@dataclass
class Project:
    name: str
    groups: list[Group]


@dataclass
class Module:
    name: str
    projects: dict[Project]


def intra_to_final() -> None:
    return


def main() -> None:
    return


if __name__ == "__main__":
    main()
