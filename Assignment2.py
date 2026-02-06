import argparse

import csv
import logging
from datetime import datetime


def downloadData(url):
    from urllib.request import urlopen
    response = urlopen(url)
    return response.read().decode("utf-8")


def processData(fileContents):
    logger = logging.getLogger("assignment2")
    personData = {}

    lines = fileContents.splitlines()
    reader = csv.reader(lines)

    for linenum, row in enumerate(reader, start=1):
        if linenum == 1:
            continue  # skip header

        try:
            person_id = int(row[0])
            name = row[1]
            birthday_str = row[2]

            birthday_dt = datetime.strptime(birthday_str, "%d/%m/%Y")
            personData[person_id] = (name, birthday_dt)

        except Exception:
            bad_id = row[0]
            logger.error(f"Error processing line #{linenum} for ID #{bad_id}")

    return personData


def displayPerson(id, personData):
    if id not in personData:
        print("No user found with that id")
        return

    name, birthday = personData[id]
    print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL to CSV file")
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print("Error downloading data:", e)
        return

    logging.basicConfig(
        filename="error.log",
        level=logging.ERROR,
        format="%(message)s"
    )

    personData = processData(csvData)

    while True:
        user_input = input("Enter an ID to lookup (<= 0 to exit): ")

        try:
            lookup_id = int(user_input)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if lookup_id <= 0:
            break

        displayPerson(lookup_id, personData)


if __name__ == "__main__":
    main()

