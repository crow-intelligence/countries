import altair as alt
import pandas as pd

alt.themes.enable("fivethirtyeight") # itt a stílust tudod állítani

df = pd.read_csv("data/processed/final.csv", sep=",")

# ha valami nem kell, akkor csak kommenteld ki
rankings = [
    # "Competitiveness",
    "GDP",
    "Business",
    "Law",
    "Science",
    "Happiness",
    # "HDI",
    # "Aggregated",
    # "Average",
]

for ranking in rankings:
    df_sorted = df.sort_values(by=ranking, ascending=True)
    top10 = df_sorted["Country"][:5] # itt adod meg hogy hány ország legyen a ploton
    df_top = df_sorted[df_sorted["Country"].isin(top10)]

    df_top = pd.melt(
        df_top,
        id_vars=["Country"],
        value_vars=rankings,
    )

    chart = (
        alt.Chart(df_top)
        .mark_line(point=True)
        .encode(
            x=alt.X("variable:N", title="ranking"),
            y=alt.Y("rank:O", scale=alt.Scale(zero=False)),
            color=alt.Color("Country:N"),
            tooltip="Country",
            strokeWidth=alt.value(40),
        )
        .transform_window(
            rank="rank()",
            sort=[alt.SortField("value", order="ascending")],
            groupby=["variable"],
        )
        .properties(
            title=f"Country Rankings top 10 by {ranking}",
            width=1500,
            height=750,
        )
    ).interactive()

    chart.save(f"vizs/bumps/{ranking}.html")
