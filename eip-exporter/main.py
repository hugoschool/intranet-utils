from argparse import ArgumentParser
from typing import Any
import requests
from requests import PreparedRequest
import json
import os
import time

BASE_URL = "https://innovation.epitech.eu/api/public/projects"

# fmt: off
DEFAULT_CITIES = [
    "BE/BRU",   # Bruxelles
    "DE/BER",   # Berlin
    "ES/BAR",   # Barcelone
    "FR/BDX",   # Bordeaux
    "FR/LIL",   # Lille
    "FR/LYN",   # Lyon
    "FR/MAR",   # Marseille
    "FR/MLH",   # Mulhouse
    "FR/MLN",   # Moulins
    "FR/MPL",   # Montpellier
    "FR/NAN",   # Nantes
    "FR/NCE",   # Nice
    "FR/NCY",   # Nancy
    "FR/PAR",   # Paris
    "FR/REN",   # Rennes
    "FR/RUN",   # La Réunion
    "FR/STG",   # Strasbourg
    "FR/TLS",   # Toulouse
]
# fmt: on


def export_eip(city: str, promotion_year: int) -> Any:
    params = {"city_code": city, "promotion": promotion_year}
    req = PreparedRequest()
    req.prepare_url(BASE_URL, params)
    req.prepare_method("GET")

    session = requests.Session()
    res = session.send(req)

    if not res.ok:
        res.raise_for_status()

    return res.json()


# Not really that great, but works
def remove_duplicates(content: Any) -> Any:
    ids: list[int] = []
    non_duped: Any = []

    for eip in content:
        if eip["id"] in ids:
            continue
        ids.append(eip["id"])
        non_duped.append(eip)

    return non_duped


def output_eip(file: str, export: Any) -> None:
    current: Any = []
    if os.path.exists(file):
        with open(file, "r+") as f:
            buffer = f.read()
            if len(buffer) > 0:
                current = json.loads(buffer)
    with open(file, "w") as f:
        merged: Any = current + export

        # Remove dupes
        merged: Any = remove_duplicates(merged)

        f.write(json.dumps(merged, indent=4))


def main() -> None:
    args = ArgumentParser()
    _ = args.add_argument(
        "-c",
        "--city",
        help="If not set, it will export all cities",
        type=str,
        required=False,
    )
    _ = args.add_argument(
        "-y", "--promotion-year", help="Promotion year", type=int, required=True
    )
    # TODO: add support for scholar year
    _ = args.add_argument(
        "-o",
        "--output",
        help="Output file",
        type=str,
        default="export.json",
        required=False,
    )
    args = args.parse_args()

    export: Any = []
    cities: list[str] = []
    if args.city is not None:
        cities.append(args.city)
    else:
        cities = DEFAULT_CITIES

    print(f"Promotion year set to {args.promotion_year}")
    for i, city in enumerate(cities):
        print(f"Exporting city {city}")
        export = export_eip(city, args.promotion_year)
        output_eip(args.output, export)
        print(f"Exported to {args.output}")
        if i < len(cities) - 1:
            # Prevent ratelimit
            time.sleep(4)


if __name__ == "__main__":
    main()
