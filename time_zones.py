import sys
import shapefile


def load_county_centroids(file_path):
    sf = shapefile.Reader(file_path)

    for record in sf.iterRecords():
        yield dict(state=record[0], county=record[2], lon=record[6], lat=record[7])


for record in load_county_centroids(sys.argv[1]):
    print(
        record["county"]
        + ", "
        + record["state"]
        + ": ("
        + str(record["lat"])
        + ","
        + str(record["lon"])
        + ")"
    )
