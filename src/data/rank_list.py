import json

import pandas as pd

df = pd.read_csv("data/interim/super_dataframe.csv", sep=",", encoding="utf-8")
df["LawRank"] = [int(e.replace("/126", "")) for e in df["LawRank"]]
df = df.drop_duplicates("Country_x", keep="first")
countries = sorted(list((df["Country_x"])))


def get_country_rank(country, ranking):
    return ranking.index(country) + 1


competitiveness = list(df.sort_values(by=["Competetiveness Rank / 141"])["Country_x"])
competitiveness_ranks = [
    get_country_rank(country, competitiveness) for country in countries
]

gdp = list(df.sort_values(by=["GDP Rank"])["Country_x"])
gdp_ranks = [get_country_rank(country, gdp) for country in countries]

business = list(df.sort_values(by=["Business Rank"])["Country_x"])
business_ranks = [get_country_rank(country, business) for country in countries]

law = list(df.sort_values(by=["LawRank"])["Country_x"])
law_ranks = [get_country_rank(country, law) for country in countries]

science = list(df.sort_values(by=["ScienceRank"])["Country_x"])
science_ranks = [get_country_rank(country, science) for country in countries]

happiness = list(df.sort_values(by=["Happiness score"])["Country_x"])
happiness.reverse()
happiness_ranks = [get_country_rank(country, happiness) for country in countries]

# freedom = list(df.sort_values(by=["Freedom Rank"])["Country_x"])
# freedom.reverse()
# freedom_ranks = [get_country_rank(country, freedom) for country in countries]

hdi = list(df.sort_values(by=["HDI rank"])["Country_x"])
hdi_ranks = [get_country_rank(country, hdi) for country in countries]

m = [competitiveness, gdp, business, law, science, happiness, hdi]
mdf = pd.DataFrame(m)
towrite = mdf.to_csv(index=False, header=False)
with open("data/interim/ranks.csv", "w") as f:
    f.write(towrite)

with open("data/interim/rankaggreg.txt", "r") as inf:
    aggregated = inf.read().strip().split(",")

aggregated_ranks = [get_country_rank(country, aggregated) for country in countries]
all_ranks = [
    competitiveness_ranks,
    gdp_ranks,
    business_ranks,
    law_ranks,
    science_ranks,
    happiness_ranks,
    # freedom_ranks,
    hdi_ranks,
    aggregated_ranks,
]
avg = [float(sum(col)) / len(col) for col in zip(*all_ranks)]
all_ranks.append(avg)
all_ranks.insert(0, countries)
all_df = pd.DataFrame(all_ranks)
header = [
    "Country",
    "Competitiveness",
    "GDP",
    "Business",
    "Law",
    "Science",
    "Happiness",
    # "Freedom",
    "HDI",
    "Aggregated",
    "Average",
]
all_write = all_df.T.to_csv(index=False, header=header)
with open("data/processed/final.csv", "w") as f:
    f.write(all_write)

