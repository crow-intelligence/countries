# Title     : Aggregate lists
# Objective : TODO
# Created by: Zoltan Varju
# Created on: 2019. 10. 29.
library('RankAggreg')
set.seed(1234567891234567891)
# 123456789123
# 12345678912345
# 123456789123456789
t <- read.table(file="/home/developer/PycharmProjects/countries/data/interim/ranks.csv", header = FALSE, sep=",")
t <- as.matrix(t)
p <- RankAggreg(t, 106, method="CE", distance="Spearman",
                N=150, convIn=5, rho=.1, verbose=TRUE)
