import requests
import json

TOKEN = input(
    'Enter your token (enter in your console: `JSON.parse(window.localStorage.getItem("@account")).token`): '
)
BASE_URL = "https://my.epitech.eu/api/"
type Project = tuple[str, int]


# Unused due to expanded = True usage
# TODO: can be used a fallback
def get_instances() -> list[int]:
    url = f"{BASE_URL}/units/instances"
    page = 1
    params = {"page": page, "schoolYear": 2026, "expanded": False}
    res = None
    instances_codes = []

    while res is None or res["meta"]["hasNext"]:
        res = requests.get(
            url, params=params, headers={"Authorization": f"Bearer {TOKEN}"}
        )

        if not res.ok:
            return instances_codes

        res = res.json()

        for data in res["data"]:
            instances_codes.append(data["unitCode"])

        page += 1

    return instances_codes


def get_project_ids_with_instance() -> list[Project]:
    url = f"{BASE_URL}/units/instances"
    page = 1
    params = {"page": page, "schoolYear": 2026, "expanded": "true"}
    res = None
    project_ids = []

    while res is None or res["meta"]["hasNext"]:
        res = requests.get(
            url, params=params, headers={"Authorization": f"Bearer {TOKEN}"}
        )

        if not res.ok:
            return project_ids

        res = res.json()

        for data in res["data"]:
            if "projectInstances" not in data:
                continue
            for project in data["projectInstances"]:
                project_ids.append((data["unitCode"], project["id"]))

        page += 1

    return project_ids


def get_info_for_project(project: Project) -> dict | None:
    url = f"{BASE_URL}/units/2026/{project[0]}/LYN-1/projects/{project[1]}"

    res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"})

    if not res.ok:
        return None

    res = res.json()

    if "registrations" not in res:
        return None

    return {"name": res["name"], "groups": res["registrations"]}


def main() -> None:
    project_ids = get_project_ids_with_instance()

    for project_id in project_ids:
        info = get_info_for_project(project_id)

        if info is None:
            continue

        with open(f"results/{info['name']}.json", "w") as f:
            f.write(
                json.dumps(
                    {
                        "meta": {"name": info["name"], "unitCode": project_id[0]},
                        "groups": info["groups"],
                    }
                )
            )


main()
