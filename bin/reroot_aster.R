require(ape)
tree <- read.tree("synechococcus_mappedWH8101.astral4.dnd")
source("../bin/mad.R")
res <- mad(write.tree(tree), output = "full")
tree <- res[[6]][[1]]
write.tree(tree, "synechococcus_mappedWH8101.astral4.mad.dnd")

png(filename="aster_tree.png")
plot(tree, no.margin = TRUE)
dev.off()
