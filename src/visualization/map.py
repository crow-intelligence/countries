import json
from shapely.geometry import Polygon
import country_converter as coco
import folium
import geopandas as gpd
import pandas as pd

cc = coco.CountryConverter()


def convert_country(country):
    return cc.convert(names=[country], to="ISO3")


rankings = [
    "Competitiveness",
    "GDP",
    "Business",
    "Law",
    "Science",
    "Happiness",
    "HDI",
    "Aggregated",
    "AverageIDX",
]

df = pd.read_csv("data/processed/clustered.csv", sep=",")
df["iso_a3"] = [convert_country(c) for c in df["Country"]]
df = df.sort_values(by="Average", ascending=True)
df["AverageIDX"] = [list(df["Average"]).index(e) + 1 for e in list(df["Average"])]

gpdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# NOTE: we have to put the data into the geodata, otherwise tooltips are too tricky
ranking_df = pd.merge(gpdf, df, on=["iso_a3"], how="outer")
ranking_df[rankings] = ranking_df[rankings].fillna(-1)
ranking_df[["geometry"]] = ranking_df[["geometry"]].fillna(Polygon([(0, 0), (0, 0), (0, 0)]))
geojson = json.loads(ranking_df.to_json())

for ranking in rankings:
    m = folium.Map()
    m = folium.Map(location=(20, 10), tiles="Stamen Toner", zoom_start=1.95)

    cp = folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=rankings,
        key_on=f"feature.properties.{ranking}"
    ).add_to(m)

    folium.LayerControl().add_to(m)
    cp.geojson.add_child(folium.features.GeoJsonTooltip(["Country"] + rankings, labels=True))
    m.save(f"vizs/maps/folium/{ranking}.html")
