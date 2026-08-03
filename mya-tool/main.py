from argparse import ArgumentParser, Namespace
from requests import PreparedRequest, Session
import json

BASE_URL = "https://epitech.campuscommunity.app"


def download_programs(args: Namespace) -> None:
    programs = []
    currentItems: int = 0
    maxItems: int = -1

    url = f"{BASE_URL}/api/v2/public/programs"
    page: int = 1
    itemsPerPage: int = 50  # Max amount of programs available on the site

    # We need to paginate all of them
    while currentItems < maxItems or maxItems == -1:
        params = {
            "typeId": "16,17,3",  # No idea what this is
            "page": page,
            "limit": itemsPerPage,
        }

        req = PreparedRequest()
        req.prepare_url(url, params)
        req.prepare_method("GET")

        session = Session()
        res = session.send(req)

        if not res.ok:
            res.raise_for_status()

        print(f"Loaded page {page}")

        json_data = res.json()
        data = json_data["data"]

        if maxItems == -1:
            maxItems = data["meta"]["totalItems"]

        programs.extend(data["programs"])

        currentItems += itemsPerPage

        page += 1

    with open(args.output, "w+") as f:
        f.write(json.dumps(programs, indent=4))
        print(f"Successfully wrote to {args.output}")


def main() -> None:
    args = ArgumentParser()
    subparsers = args.add_subparsers(dest="subparser_name")

    download_args = subparsers.add_parser("download")
    _ = download_args.add_argument(
        "-o",
        "--output",
        help="Output file",
        type=str,
        default="programs.json",
        required=False,
    )

    args = args.parse_args()

    if args.subparser_name is None:
        raise ValueError("Missing subcommand")

    commands = {"download": download_programs}

    commands[args.subparser_name](args)


if __name__ == "__main__":
    main()
