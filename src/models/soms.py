import pandas as pd
import SimpSOM as sps


df = pd.read_csv("data/processed/final.csv",
                 sep=",")
labels = df["Country"]
df = df.drop(["Country", "Aggregated", "Average"], axis=1)

net = sps.somNet(20, 20, df.values, PBC=True, PCI=True)
net.train(0.1, 10000)
net.save('somweights')
net.nodes_graph(colnum=6)
net.diff_graph()

net.cluster(df.values, type='qthresh')
#net.diff_graph(show=True, printout=True)

