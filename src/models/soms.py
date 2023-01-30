import pandas as pd
import simpsom as sps

df = pd.read_csv("data/processed/final.csv", sep=",")
labels = df["Country"]
df = df.drop(["Country", "Aggregated", "Average"], axis=1)

net = sps.SOMNet(
    50,
    50,
    df.values,
    topology="hexagonal",
    init="PCA",
    metric="cosine",
    neighborhood_fun="gaussian",
    PBC=True,
    random_seed=32,
    GPU=False,
    CUML=False,
    output_path="models",
)
net.train(train_algo="batch", start_learning_rate=0.01, epochs=-1, batch_size=-1)

net.save_map("trained_som.npy")

projection = net.project_onto_map(df)
# cls = net.cluster(net) # TODO: fixme!!!!!!
