import pickle
import pandas as pd
import SimpSOM as sps
from PIL import Image, ImageChops


df = pd.read_csv("data/processed/final.csv",
                 sep=",")
labels = df["Country"]
df = df.drop(["Country", "Aggregated", "Average"], axis=1)

net = sps.somNet(20, 20, df.values, PBC=True, PCI=True)
#net = sps.somNet(40, 40, df.values, PBC=True, PCI=True, loadFile="somweights")
net.train(0.1, 10000)
net.save('somweights')
# net.nodes_graph(colnum=6)
# net.diff_graph()

net.cluster(df.values, type='qthresh')
net.diff_graph(show=True, printout=True)


# Here we first define a few useful functions
def autocrop(fileName):
    im = Image.open(fileName)
    im = im.crop((0, 100, 2900, im.size[1]))
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

projData = net.project(df.values)
cropped = autocrop('nodesDifference.png')
cropped.save('cropped.png')

with open("projData.pkl", "wb") as f:
    pickle.dump(projData, f)
