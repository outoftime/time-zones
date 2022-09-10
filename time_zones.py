import sys
import shapefile

sf = shapefile.Reader(sys.argv[1])

for record in sf.iterRecords():
    state = record[0]
    county = record[2]
    lon = record[6]
    lat = record[7]
    print(county + ", " + state + ": (" + str(lat) + "," + str(lon) + ")")
