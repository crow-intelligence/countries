import altair as alt
import country_converter as coco
import geopandas as gpd
import gpdvega
import pandas as pd

cc = coco.CountryConverter()


def convert_country(country):
    return cc.convert(names=[country], to="ISO3")


alt.themes.enable("fivethirtyeight")

df = pd.read_csv("data/processed/clustered.csv", sep=",")
df["iso_a3"] = [convert_country(c) for c in df["Country"]]
df = df.sort_values(by="Average", ascending=True)
df["AverageIDX"] = [list(df["Average"]).index(e) + 1 for e in list(df["Average"])]

rankings_types = [
    "Competitiveness:O",
    "GDP:O",
    "Business:O",
    "Law:O",
    "Science:O",
    "Happiness:O",
    "HDI:O",
    "Aggregated:O",
    "AverageIDX:O",
    "Country:N",
]

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

gpdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

ranking_df = pd.merge(gpdf, df, on=["iso_a3"], how="outer")
ranking_df[rankings] = ranking_df[rankings].fillna(-1)

for ranking in rankings:
    chart = (
        alt.Chart(ranking_df[ranking_df["continent"] != "Antarctica"])
        .mark_geoshape()
        .project()
        .encode(
            color=alt.Color(f"{ranking}:Q", scale=alt.Scale(scheme="dark2")),
            tooltip=rankings_types,
        )
        .properties(width=1200, height=600)
    )

    chart.save(f"vizs/maps/altair/{ranking}.html")
