import altair as alt
import pandas as pd

df = pd.read_csv("data/processed/final.csv", sep=",")

rankings = [
    "Competitiveness",
    "GDP",
    "Business",
    "Law",
    "Science",
    "Happiness",
    "HDI",
    "Aggregated",
    "Average",
]

for ranking in rankings:
    df_sorted = df.sort_values(by=ranking, ascending=True)
    top10 = df_sorted["Country"][:10]
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
            x=alt.X("variable:O", title="ranking"),
            y="rank:O",
            color=alt.Color("Country:N"),
            tooltip="Country",
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

    chart.save(f"vizs/{ranking}.html")
