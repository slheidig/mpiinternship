library(ggplot2)
library(dplyr)

args = commandArgs(trailingOnly=TRUE)

eig <- sqrt(unlist(read.table(paste(paste(args[1],"smartPCA", sep='_'),paste(args[1],"selection.pruned.eval", sep='.'),sep='/'),
                              stringsAsFactors = FALSE))[1:args[2]])


png(paste(paste(args[1],'pca_variance',sep='_'),"png",sep='.'))
p <- plot(eig/sum(eig), type = "b", pch = 19, 
     ylab = "Proportion of variance",
     xlab = "Principal components")
dev.off()
pca <- read.table(paste(paste(args[1],"smartPCA", sep='_'),paste(args[1],"selection.pruned.evec", sep='.'),sep='/'), stringsAsFactors = FALSE)
names(pca) <- c("ID", paste("PC", (1:(ncol(pca)-2)), sep=""), "case.control")
pca <- pca[,1:(ncol(pca)-1)] # Remove case/control column

pca$SampleID <- sapply(strsplit(pca$ID, split = ":"), function(x) x[2])

p12 <- ggplot(pca,  aes(x = PC1, y = PC2, color=SampleID)) + 
    geom_point()
p12 <- ggsave(paste(paste(args[1],'pca_12',sep='_'),"png",sep='.'))

p34 <- ggplot(pca,  aes(x = PC3, y = PC4, color=SampleID)) + 
    geom_point()
p34 <- ggsave(paste(paste(args[1],'pca_34',sep='_'),"png",sep='.'))