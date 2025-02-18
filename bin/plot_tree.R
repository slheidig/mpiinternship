require(ape)
tree <- read.tree("andi/andi_distances_formated.phy_fastme_tree.nwk")
require(phangorn)
tree <- midpoint(tree)
write.tree(tree, "andi/andi_tree.dnd")

png(filename="andi/andi_tree.png")
plot(tree, no.margin = TRUE, x.lim=0.35)
dev.off()
