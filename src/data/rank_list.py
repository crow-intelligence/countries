import pandas as pd

df = pd.read_csv("data/interim/super_dataframe.csv", sep=",", encoding="utf-8")
competitiveness = ["None"] * 110
gdp = ["None"] * 110
business = ["None"] * 110
law = ["None"] * 110
science = ["None"] * 110
happiness = ["None"] * 110
freedom = ["None"] * 110

countries = list(df["Country_x"])

for index, row in df.iterrows():
    country = countries[index]
    competitiveness_rank = row["Competitiveness Rank"] - 1
    competitiveness[competitiveness_rank] = country
    gdp_rank = row["GDP Rank"] - 1
    gdp[gdp_rank] = country
    business_rank = row["Business Rank"] - 1
    business[business_rank] = country
    law_rank = row["Law Rank"] - 1
    law[law_rank] = country
    science_rank = row["Science Rank"] - 1
    science[science_rank] = country
    happiness_rank = row["Happiness Rank"] - 1
    happiness[happiness_rank] = country
    freedom_rank = row["Freedom Rank"] - 1
    freedom[freedom_rank] = country

m = [competitiveness, gdp, business, law, science, happiness, freedom]
mdf = pd.DataFrame(m)
towrite = mdf.to_csv(index=False, header=False)
with open("data/interim/ranks.csv", "w") as f:
    f.write(towrite)
