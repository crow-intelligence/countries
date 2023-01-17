import pickle

import country_converter as coco
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

cc = coco.CountryConverter()


def convert_country(country):
    return cc.convert(names=[country], to="ISO3")


with open("projData.pkl", "rb") as f:
    projdata = pickle._load(f)


df = pd.read_csv("data/processed/final.csv", sep=",")

labels = list(df["Country"])
country_cluster = {}
i = 0
with open("qthresh_clusters.dat", "r") as f:
    for l in f:
        l = l.strip().split()
        l = [int(e) for e in l]
        countries = [labels[i] for i in l]
        for country in countries:
            country_cluster[country] = str(i)
        i += 1

clusters = [country_cluster[country] for country in labels]
country_codes_iso3 = [convert_country(country) for country in labels]
df["Clusters"] = clusters
df["ISO3"] = country_codes_iso3

all_write = df.to_csv(index=False)
with open("data/processed/final_with_clusters.csv", "w") as f:
    f.write(all_write)
x_coords = [x for x, y in projdata]
y_coords = [y for x, y in projdata]

comp = list(df["Competitiveness"])
gdp = list(df["GDP"])
business = list(df["Business"])
law = list(df["Law"])
science = list(df["Science"])
happiness = list(df["Happiness"])
freedom = list(df["Freedom"])
hdi = list(df["HDI"])
avg = list(df["Average"])
aggregated = list(df["Aggregated"])

header_labels = list(df.columns)
h = [
    "Country",
    "ISO3",
    "Competitiveness",
    "GDP",
    "Business",
    "Law",
    "Science",
    "Happiness",
    "Freedom",
    "HDI",
    "Average",
    "Aggregated",
    "Cluster",
]
ranks = list(
    zip(
        labels,
        country_codes_iso3,
        comp,
        gdp,
        business,
        law,
        science,
        happiness,
        freedom,
        hdi,
        avg,
        aggregated,
        clusters,
    )
)

legends = []
for i in range(len(ranks)):
    data = ranks[i]
    text = list(zip(h, data))
    text = [(str(e[0] + ":"), str(e[1])) for e in text]
    text = [" ".join(e) for e in text]
    text = "<br>".join(text)
    legends.append(text)

###############################################################################
###  Source: https://www.kaggle.com/asparago/unsupervised-learning-with-som  ##
###############################################################################
trace0 = go.Scatter(
    x=x_coords,
    y=y_coords,
    hoveron=labels,
    text=legends,
    mode="markers",
    marker=dict(size=8, color=clusters, colorscale="Jet", showscale=False, opacity=1),
    showlegend=False,
)
data = [trace0]

layout = go.Layout(
    images=[
        dict(
            source="cropped.png",
            xref="x",
            yref="y",
            x=-0.5,
            y=39.5 * 2 / np.sqrt(3) * 3 / 4,
            sizex=40.5,
            sizey=40 * 2 / np.sqrt(3) * 3 / 4,
            sizing="stretch",
            opacity=0.8,
            layer="below",
        )
    ],
    width=800,
    height=800,
    hovermode="closest",
    xaxis=dict(
        range=[-1, 41], zeroline=False, showgrid=False, ticks="", showticklabels=False
    ),
    yaxis=dict(
        range=[-1, 41], zeroline=False, showgrid=False, ticks="", showticklabels=False
    ),
    showlegend=True,
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename="styled-scatter.html")
