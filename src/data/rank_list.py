import json

import pandas as pd

df = pd.read_csv("data/interim/super_dataframe.csv", sep=",", encoding="utf-8")
competitiveness = ["None"] * 106
gdp = ["None"] * 106
business = ["None"] * 106
law = ["None"] * 106
science = ["None"] * 106
happiness = ["None"] * 106
freedom = ["None"] * 106

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

with open("data/interim/ranaggreg.txt", "r") as inf:
    aggregated = inf.read().strip().split(",")

aggregated_ranks = [aggregated.index(e)+1 for e in countries]
df["Aggregated Rank"] = aggregated_ranks
finalcsv = df.to_csv(index=False)
with open("data/processed/fullranking.csv", "w") as outfile:
    outfile.write(finalcsv)

# json
# var myData = [
# 	{
# 		key: "UK",
# 		values: [
# 			{ key: "Apples", value: 9 },
# 			{ key: "Oranges", value: 3 },
# 			{ key: "Pears", value: 5 },
# 			{ key: "Bananas", value: 7 }
# 		]
# 	},
# 	{
# 		key: "France",
# 		values: [
# 			{ key: "Apples", value: 5 },
# 			{ key: "Oranges", value: 4 },
# 			{ key: "Pears", value: 6 },
# 			{ key: "Bananas", value: 2 }
# 		]
# 	}
# ];
mydata = []
data = eval(df.to_json(orient='records'))
for e in data:
    values = []
    ks = ["Happiness Rank", "Freedom Rank", "Competitiveness Rank",
          "GDP Rank", "Business Rank", "Law Rank", "Science Rank",
          "Aggregated Rank"]
    for k in ks:
        kv = {"key": k, "value": abs(e[k]-106)+1}
        values.append(kv)
    elem = {"key": e["Country_x"],
            "values": values}
    mydata.append(elem)


with open('data/processed/ranking.json', 'w') as outfile:
    json.dump(mydata, outfile)