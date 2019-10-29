# Title     : Aggregate lists
# Objective : TODO
# Created by: Zoltan Varju
# Created on: 2019. 10. 29.
library('RankAggreg')
set.seed(100)
aggreg_mlt <- function(m, n) {
  mm <- as.matrix(m)
  t <- RankAggreg(mm, n, method="CE", distance="Spearman",
                  N=106, convIn=5, rho=.1, verbose=FALSE)
  return(t[1])
}

t <- read.csv(file="/home/developer/PycharmProjects/countries/data/interim/ranks.csv", header = False)

res <- aggreg_mlt(t, 106)
