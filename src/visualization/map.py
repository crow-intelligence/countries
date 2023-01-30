import country_converter as coco
import folium
import pandas as pd

cc = coco.CountryConverter()


def convert_country(country):
    return cc.convert(names=[country], to="ISO3")


df = pd.read_csv("data/processed/clustered.csv", sep=",")
df["ISO3"] = [convert_country(c) for c in df["Country"]]

political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

m = folium.Map()
m = folium.Map(location=(20, 10), tiles="Stamen Toner", zoom_start=1.95)

# folium.GeoJson(political_countries_url).add_to(m)
folium.Choropleth(
    geo_data=political_countries_url,
    data=df,
    columns=["ISO3", "clusters"],
    key_on="feature.properties.adm0_a3", # adm0_a3 --> iso-3
    fill_color="PuBuGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Country rankings",
    name="Country rankings"
).add_to(m)
folium.LayerControl().add_to(m)

m.save("vizs/maps/test.html")