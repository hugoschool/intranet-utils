from argparse import ArgumentParser, Namespace
from datetime import datetime
from requests import PreparedRequest, Session
from typing import Any
import json

BASE_URL = "https://epitech.campuscommunity.app"
FRONTEND_BASE_URL = "https://epitech.globalcampus.app"


TAG_GPA = "GPA Requirement"
TAG_SPOTS = "Available Spots"
TAG_DUAL_DEGREE = "Dual degree/certificate proposed"


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


def load_programs(input_file: str):
    with open(input_file, "r") as f:
        return json.loads(f.read())


class Destinations:
    def __init__(self, args: Namespace):
        self.args = args
        self.content = load_programs(args.input)

        subcommands = {"country": self.list_all_countries, "school": self.school}

        subcommands[args.destinations_subparser_name]()

    @staticmethod
    def arguments(args):
        _ = args.add_argument(
            "-i",
            "--input",
            help="Input file",
            type=str,
            default="programs.json",
            required=False,
        )

        subparsers = args.add_subparsers(dest="destinations_subparser_name")
        country_args = subparsers.add_parser("country")  # noqa: F841

        school_args = subparsers.add_parser("school")

        _ = school_args.add_argument(
            "--filter",
            help="Filter out only the columns that you wish to have in your final CSV. Seperated by comma (,) (by default: all columns)",
            type=str,
            required=False,
        )

        _ = school_args.add_argument(
            "--delimiter",
            help="CSV Delimiter",
            type=str,
            default=";",
            required=False,
        )
        _ = school_args.add_argument(
            "--country",
            help="Name of the country",
            type=str,
            default="",
            required=False,
        )

    @staticmethod
    def replace_country_aliases(country: str) -> str:
        aliases = {"UK": "United Kingdom", "USA": "United States of America"}

        if country in aliases:
            return aliases[country]
        return country

    @staticmethod
    def correct_price(price: float) -> float:
        return price / 100

    @staticmethod
    def amount_days_between(startDate: str, endDate: str) -> int:
        try:
            startDate = startDate.split("T")[0]
            endDate = endDate.split("T")[0]

            startDate = datetime.strptime(startDate, "%Y-%m-%d")
            endDate = datetime.strptime(endDate, "%Y-%m-%d")

            return (endDate - startDate).days
        except:  # noqa: E722
            return -1

    @staticmethod
    def get_from_tags(tags: list, name: str) -> Any | None:
        for tag in tags:
            if tag["parent"]["name"] == name:
                try:
                    return tag["name"]
                except ValueError:
                    return None

        return None

    def print(self, array) -> None:
        for i, item in enumerate(array):
            print(item, end="")
            if i < len(array) - 1:
                print(self.args.delimiter, end="")
        print()

    def list_all_countries(self) -> None:
        countries: set[str] = set()

        for program in self.content:
            for location in program["locations"]:
                countries.add(location["label"])

        countries = list(countries)
        countries.sort()

        for country in countries:
            print(country)

    def school(self) -> None:
        selected_country = ""
        if self.args.country is not None:
            selected_country = self.replace_country_aliases(self.args.country)

        schools = []

        for program in self.content:
            locations = set()

            for location in program["locations"]:
                locations.add(location["label"])

            if selected_country == "" or selected_country in locations:
                schools.append(program)

        info = {
            "name": None,
            "price": None,
            "days_amount": None,
            "gpa": None,
            "spots": None,
            "dual_degree": None,
            "link": None,
        }

        columns = []

        if self.args.filter is not None:
            columns = self.args.filter.split(",")

            for column in columns:
                if column not in info:
                    columns.remove(column)

        if len(columns) == 0:
            for elem in info:
                columns.append(elem)

        for i, school in enumerate(schools):
            info["name"] = school["name"]
            info["price"] = self.correct_price(school["priceCents"])
            info["days_amount"] = self.amount_days_between(
                school["startDate"], school["endDate"]
            )
            info["gpa"] = self.get_from_tags(school["tags"], TAG_GPA)
            info["spots"] = self.get_from_tags(school["tags"], TAG_SPOTS)
            info["dual_degree"] = self.get_from_tags(school["tags"], TAG_DUAL_DEGREE)
            info["link"] = f"{FRONTEND_BASE_URL}/programs/{school['id']}"

            if i == 0:
                self.print(columns)

            print_values = []

            for column in columns:
                print_values.append(info[column])

            self.print(print_values)


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

    destinations_args = subparsers.add_parser("destinations")
    Destinations.arguments(destinations_args)
    args = args.parse_args()

    if args.subparser_name is None:
        raise ValueError("Missing subcommand")

    commands = {
        "download": download_programs,
        "destinations": Destinations,
    }

    commands[args.subparser_name](args)


if __name__ == "__main__":
    main()
