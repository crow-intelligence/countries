# Title     : Aggregate lists
# Objective : TODO
# Created by: Zoltan Varju
# Created on: 2019. 10. 29.
library('RankAggreg')
set.seed(42)

t <- read.table(file="/home/zoli/PycharmProjects/countries/data/interim/ranks.csv", header = FALSE, sep=",")
t <- as.matrix(t)
p <- RankAggreg(t, 106, method="CE", distance="Spearman",
                N=110, convIn=5, rho=.1, verbose=TRUE)
