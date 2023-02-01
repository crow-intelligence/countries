import altair as alt
import pandas as pd

alt.themes.enable("fivethirtyeight")

df = pd.read_csv("data/processed/final.csv", sep=",")
df_sorted = df.sort_values(by="Average", ascending=True)
df_sorted["AverageIDX"] = [
    list(df_sorted["Average"]).index(e) + 1 for e in list(df_sorted["Average"])
]

top = df_sorted["Country"][:106]
df_top = df_sorted[df_sorted["Country"].isin(top)]

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


df_melted = pd.melt(
    df_top,
    id_vars=["Country"],
    value_vars=rankings,
)

df_melted["size"] = [30 for _ in range(len(df_melted["Country"]))]
chart = (
    alt.Chart(df_melted)
    .mark_circle()
    .encode(
        x="Country:N",
        y="value:O",
        size=alt.Size("size", legend=None),
        color="variable:N",
        tooltip=["Country:N", "variable:N", "value:O"],
    )
).interactive()

chart.save("vizs/punchcards/punch_card.html")
