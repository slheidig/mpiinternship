require(ape)
tree <- read.tree("syn_pop1_mappedBOUM118.astral4.dnd")
source("../bin/mad.R")
res <- mad(write.tree(tree), output = "full")
tree <- res[[6]][[1]]
write.tree(tree, "syn_pop1_mappedBOUM118.astral4.mad.dnd")

png(filename="aster_tree.png")
plot(tree, no.margin = TRUE)
dev.off()
