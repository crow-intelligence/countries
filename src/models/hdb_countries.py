import hdbscan
import pandas as pd

df = pd.read_csv("data/processed/final.csv", sep=",")

clusterer = hdbscan.HDBSCAN(min_cluster_size=2, gen_min_span_tree=True)
clusterer.fit(df.drop(columns=["Country"]))

df["clusters"] = clusterer.labels_

df.to_csv("data/processed/clustered.csv", sep=",", index=False)
