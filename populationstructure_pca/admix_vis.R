####BROKEN
args = commandArgs(trailingOnly=TRUE)


tbl <- read.table(paste(args[1],"selection.pruned.2.Q", sep='.'))
tbl2 <- t(as.matrix(tbl))
print(tbl)

labels <- read.table(paste(args[1],"selection.pruned.fam", sep='.'))[,2]

print(labels)
colnames(tbl) <- labels

print(tbl)

print(tbl2)
barplot(tbl2, col=rainbow(2), xlab="Individual #", ylab="Ancestry", border=NA, las=2)