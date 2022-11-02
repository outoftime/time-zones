# Optimal time zone calculator

This script populates optimal time zones for the United States based on an ideal solar noon window of noon—1pm. See http://outoftime.github.io/time-zones for a full description of the approach.

## Running the script

Install the dependencies:

$ pip install -r requirements.txt

You’ll need to download the data sets. You can get the county population data set [here](https://www2.census.gov/programs-surveys/popest/datasets/2020-2021/counties/totals/co-est2021-alldata.csv), and the county shapefiles [here](https://www.weather.gov/source/gis/Shapefiles/County/c_13se22.zip). Unzip the shapefile archive, and put everything in a folder called `data/`.

Now run it like this:

```sh
$ python time_zones.py data/c_13se22/c_13se22 data/co-est2021-alldata.csv
```
