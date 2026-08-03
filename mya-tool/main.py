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
            "--name",
            help="List only names",
            action="store_true",
            default=False,
            required=False,
        )
        _ = school_args.add_argument(
            "--price",
            help="List only prices",
            action="store_true",
            default=False,
            required=False,
        )
        _ = school_args.add_argument(
            "--country",
            help="Name of the country",
            type=str,
            default="",
            required=False,
        )

    def verify_country(self):
        if "country" not in self.args or self.args.country == "":
            raise ValueError("Missing destination country")

    @staticmethod
    def replace_country_aliases(country: str) -> str:
        aliases = {"UK": "United Kingdom", "USA": "United States of America"}

        if country in aliases:
            return aliases[country]
        return country

    @staticmethod
    def correct_price(price: float) -> float:
        return price / 100

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
        self.verify_country()
        country = self.replace_country_aliases(self.args.country)

        schools = []

        for program in self.content:
            locations = set()

            for location in program["locations"]:
                locations.add(location["label"])

            if country in locations:
                schools.append(program)

        for school in schools:
            if self.args.name:
                print(school["name"])
            elif self.args.price:
                print(self.correct_price(school["priceCents"]))
            else:
                print(f"{school['name']},{self.correct_price(school['priceCents'])}")


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
