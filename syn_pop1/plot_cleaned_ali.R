

dat1 <- read.csv("FilteredAlignments/syn_pop1_mappedBOUM118.statistics.csv", sep="\t")
dat2 <- read.csv("FilteredAlignments/syn_pop1_mappedBOUM118.subset-statistics.csv", sep="\t")
dat3 <- read.csv("FilteredAlignments/syn_pop1_mappedBOUM118.realigned-statistics.csv", sep="\t")
dat4 <- read.csv("FilteredAlignments/syn_pop1_mappedBOUM118.subset_strict-statistics.csv", sep="\t")
dat5 <- read.csv("FilteredAlignments/syn_pop1_mappedBOUM118.filtered-statistics.csv", sep="\t")

plot(table(dat1$BlockSize))
plot(table(dat2$BlockSize))
plot(table(dat3$BlockSize))
plot(table(dat4$BlockSize))
plot(table(dat5$BlockSize))

sum(dat1$BlockLength) # 1,116,290
sum(dat2$BlockLength) # 973,805
sum(dat3$BlockLength) # 909,709
sum(dat4$BlockLength) # 488,742 'core' genome
sum(dat5$BlockLength) # 450,663 cleaned 'core' genome

summary(dat4$BlockLength)
#  Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#   1.0    88.0   370.5   483.9   680.0  7387.0 