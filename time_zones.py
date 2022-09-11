from collections import defaultdict
import re
import sys
import shapefile
import csv

STATE_ABBREVIATIONS = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


def normalize_county(county):
    in_match = re.match(".+ in (.+)", county)
    if in_match:
        return normalize_county(in_match[1])
    return re.sub(
        "[ .']",
        "",
        re.sub(
            "(^City of | (Borough|County|City|City County|City and Borough|Parish|Census Area|Municipality)$|\\(.+\\))",
            "",
            county,
            flags=re.I,
        ).lower(),
    ).replace("ñ", "n")


def load_county_centroids(file_path):
    sf = shapefile.Reader(file_path)

    for record in sf.iterRecords():
        yield dict(state=record[0], county=record[2], lon=record[6], lat=record[7])


def load_county_populations(file_path):
    with open(file_path, mode="r", encoding="ISO-8859-1") as file:
        csv_file = csv.reader(file)

        next(csv_file)
        for row in csv_file:
            if row[4] != "000":  # state total
                yield dict(state=row[5], county=row[6], population=row[9])


def merge_county_records(county_centroids, county_populations):
    grouped_centroids = defaultdict(lambda: dict())
    for record in county_centroids:
        grouped_centroids[record["state"]][normalize_county(record["county"])] = record

    grouped_merged_records = defaultdict(lambda: [])

    for population_record in county_populations:
        state = STATE_ABBREVIATIONS[population_record["state"]]
        county = normalize_county(population_record["county"])
        try:
            centroid_record = grouped_centroids[state][county]
            grouped_merged_records[state].append(
                dict(
                    state=state,
                    county=population_record["county"],
                    lat=centroid_record["lat"],
                    lon=centroid_record["lon"],
                    population=population_record["population"],
                )
            )
        except:
            print(
                "Could not find matching centroid record for "
                + county
                + ", "
                + state
                + " ("
                + population_record["county"]
                + ")."
            )
            print("Available counties: " + str(grouped_centroids[state].keys()))

    return grouped_merged_records


if __name__ == "__main__":
    county_centroids = load_county_centroids(sys.argv[1])

    county_populations = load_county_populations(sys.argv[2])

    for a, b in merge_county_records(county_centroids, county_populations).items():
        print(a)
        print(b)
