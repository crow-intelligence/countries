import country_converter as coco
import pandas as pd

cc = coco.CountryConverter()


def convert_country(country):
    return cc.convert(names=[country], to="ISO3")


# read data
happiness_df = pd.read_excel("data/raw/Chapter2OnlineData.xlsx", sheet_name="Figure2.6")


happiness_names = list(happiness_df["Country"])
happiness_codes = [convert_country(n) for n in happiness_names]
happiness_df["ISO3"] = happiness_codes

competitiveness_df = pd.read_csv(
    "data/raw/competitiveness.csv", encoding="utf-8", sep="\t"
)
competitiveness_names = list(competitiveness_df["Country / Economy"])
competitiveness_codes = [convert_country(n) for n in competitiveness_names]
competitiveness_df["ISO3"] = competitiveness_codes

freedom_df = pd.read_csv("data/raw/fiw.csv", encoding="utf-8", sep="\t")
freedom_names = list(freedom_df["Country or Territory"])
freedom_codes = [convert_country(n) for n in freedom_names]
freedom_df["ISO3"] = freedom_codes

gdp_df = pd.read_csv("data/raw/gdp_ppp.csv", encoding="utf-8", sep="\t")
gdp_names = list(gdp_df["Country"])
gdp_codes = [convert_country(n) for n in gdp_names]
gdp_df["ISO3"] = gdp_codes

business_df = pd.read_excel("data/raw/Rankings.xlsx", sheet_name="Sheet1")
business_names = business_df["Economy"]
business_codes = [convert_country(n) for n in business_names]
business_df["ISO3"] = business_codes

law_df = pd.read_csv("data/raw/rol.csv", encoding="utf-8", sep="\t")
law_names = list(law_df["Country"])
law_codes = [convert_country(n) for n in law_names]
law_df["ISO3"] = law_codes

science_df = pd.read_csv("data/raw/scimagojr.csv", encoding="utf-8", sep="\t")
science_names = list(science_df["Country"])
science_codes = [convert_country(n) for n in science_names]
science_df["ISO3"] = science_codes

geo_df = pd.read_csv("data/raw/country-capitals.csv", encoding="utf-8", sep=",")
geo_names = list(geo_df["CountryName"])
geo_codes = [convert_country(n) for n in geo_names]
geo_df["ISO3"] = geo_codes

hdi_df = pd.read_excel(
    "data/raw/HDR21-22_Statistical_Annex_HDI_Table.xlsx",
    na_values=["n.a", "NaN"],
)
hdi_df = hdi_df.dropna()
hdi_names = list(hdi_df["Country"])
hdi_codes = [convert_country(n) for n in hdi_names]
hdi_df["ISO3"] = hdi_codes


super_df = pd.merge(happiness_df, competitiveness_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, freedom_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, gdp_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, business_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, law_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, science_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, geo_df, left_on="ISO3", right_on="ISO3")
super_df = pd.merge(super_df, hdi_df, left_on="ISO3", right_on="ISO3")

# super_df["Freedom Rank"] = super_df["Aggregate Score"].rank(method="max")
t = super_df.to_csv(index=False)
with open("data/interim/super_dataframe.csv", "w") as f:
    f.write(t)
