import csv
import os
import pathlib
import sys

import httpx
from django.conf import settings
from django.core.management import BaseCommand

DATA_DIR = settings.BASE_DIR / "temp-data"
CHUNK_SIZE = 16 * 1024


class Command(BaseCommand):
    help = "Get domain information from notify"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--url", type=str, help="URL of data to upload")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        download_and_parse_domains(url)


def save_url_to_data_dir(url):
    """
    Downloads the file to the data directory
    Args:
        url: The url given in the command to download the CSV from

    Returns:
        A filepath that points to the downloaded file
    """
    filename = pathlib.Path(url).stem
    filepath = DATA_DIR / "".join((filename, pathlib.Path(url).suffix))
    if not filepath.exists():
        print(f"Downloading to: {filepath}")  # noqa: T201
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open("wb") as f:
            with httpx.stream("GET", url) as response:
                for chunk in response.iter_bytes(CHUNK_SIZE):
                    f.write(chunk)
    else:
        print(f"Skipping download: {filepath} already exists")  # noqa: T201
    return filepath


def get_sheet_headers(filename):
    """
    Gets the headers from the given file
    Args:
        filename: The given filename to read from

    Returns:
        A list of headers from the given CSV
    """
    file_extension = os.path.splitext(filename)[1]
    if file_extension.endswith(".csv"):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            headers = [header for header in headers if header != ""]
    else:
        print("The uploaded file must be a CSV file")  # noqa: T201
        sys.exit(1)
    return headers


def get_data_rows(filename):
    """
    Takes in a filename and returns the rows of that CSV
    Args:
        filename: The filename to take rows from

    Returns:
        A list of rows that contain all the data of the given CSV
    """
    data = []
    file_extension = os.path.splitext(filename)[1]
    if file_extension.endswith(".csv"):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            _ = next(reader)
            for row in reader:
                data.append(row)
    else:
        print("The uploaded file must be a CSV file")  # noqa: T201
        sys.exit(1)
    return data


def download_and_parse_domains(url):
    """
    Parses the data rows of the file to get the domain
    Args:
        url: The url to get the file from
    """
    filename = save_url_to_data_dir(url)
    headers = get_sheet_headers(filename)
    rows = get_data_rows(filename)
    # Prints the value out to the console in a format that can be copy-pasted into any file you want
    print("CIVIL_SERVICE_DOMAINS = frozenset([")
    for row in rows:
        print(f'    "{row[2]}",')

    print("])")
