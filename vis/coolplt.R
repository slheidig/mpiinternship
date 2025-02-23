# Required libraries
library(ape)
library(ggtree)
library(dplyr)
library(ggplot2)
library(tidyr)
library(ggnewscale)
library(RColorBrewer)
library(viridis)

# ------------------------------
# Function: map_input
# ------------------------------
map_input <- function(tree_file, csv_file) {
  # Read the tree
  tree <- read.tree(tree_file)

  # Read the categories CSV
  categories <- read.csv(csv_file, stringsAsFactors = FALSE)

  # Improved partial matching: check if strain_name is a substring of the tree tip label
  matched_names <- sapply(tree$tip.label, function(tip) {
    match_idx <- which(sapply(categories$strain_name, function(name) grepl(name, tip, ignore.case = TRUE)))
    if (length(match_idx) >= 1) {
      return(categories$strain_name[match_idx[1]])  # Take the first match
    } else {
      return(NA)
    }
  })

  # Print unmatched tips for debugging
  unmatched <- tree$tip.label[is.na(matched_names)]
  if (length(unmatched) > 0) {
    message("Unmatched tree tips:", paste(unmatched, collapse = ", "))
  }

  # Update tree tip labels with matched names, keep original if no match
  tree$tip.label <- ifelse(!is.na(matched_names), matched_names, tree$tip.label)

  # Filter categories to include only matched names
  categories <- categories %>% filter(strain_name %in% tree$tip.label)
  list(tree = tree, categories = categories)
}

# ------------------------------
# Function: prepare_heatmap_data
# ------------------------------
prepare_heatmap_data <- function(tree, categories) {
  # Reorder categories to match tree tip order
  categories <- categories %>%
    mutate(name = factor(strain_name, levels = tree$tip.label)) %>%
    arrange(name)

  categories
}

# ------------------------------
# Function: create_plot
# ------------------------------
create_plot <- function(tree, heatmap_data, output_csv = "heatmap_wide.csv") {
  # Plot the phylogenetic tree
  t <- ggtree(tree) + 
    geom_text(aes(label=label), hjust=-.2,size = 2) 


  # Prepare the data for heatmaps
  # Map categorical variables to color
  df_clade <- data.frame(clade = factor(heatmap_data$clade_species))
  df_ocean <- data.frame(ocean = factor(heatmap_data$isolation_ocean))
  df_temp <- data.frame(temp = heatmap_data$isolation_temperature)

  # Combine latitude and longitude into a new column for plotting
  df_lat_lon <- data.frame(lat_lon = paste(heatmap_data$Isolation_latitude_N, heatmap_data$Isolation_longitude_E, sep="-"))

  # Assign rownames to match the tree tip labels
  rownames(df_clade) <- tree$tip.label
  rownames(df_ocean) <- tree$tip.label
  rownames(df_temp) <- tree$tip.label
  rownames(df_lat_lon) <- tree$tip.label

  # Plot clade heatmap
  p1 <- gheatmap(t, df_clade, offset=.2, width=.2,colnames_offset_y = -.5) +
      scale_fill_viridis_d(option="H", name="Clade")

  # Add new scale for ocean heatmap
  p2 <- p1 + new_scale_fill()
  p2 <- gheatmap(p2, df_ocean, offset=.6, width=.2, colnames_offset_y = -.5) +
      scale_fill_viridis_d(option="D", name="Ocean")
  # Add new scale for temperature heatmap
  p3 <- p2 + new_scale_fill()

  p3 <- gheatmap(p3, df_temp, offset=1, width=.2, colnames_offset_y = -.5) +
      scale_fill_viridis(option="C", name="Temperature")
  
  # Add new scale for latitude-longitude heatmap
  #p4 <- p3 + new_scale_fill()

  #p4 <- gheatmap(p4, df_lat_lon, offset=2, width=.2,colnames_offset_y = -.5 ,colnames_angle=45) +
  #    scale_fill_viridis_d(option="B", name="Lat-Lon")

  p3 <- p3 + theme(
      legend.position = "bottom",        # Place legends at the bottom
      legend.box = "vertical",         # Set legends side by side (horizontal)
      legend.box.spacing = unit(0.2, "cm") , # Add some space between legends
      legend.key.size = unit(0.5, "cm"),
      legend.spacing.y= unit(0.05, "cm"),
    ) #+ 
  #guides(fill = guide_legend( nrow = 3))#+
    #guides(fill = guide_colorbar(barwidth = 5, barheight = 0.5, title.position = "top"))

  # Final plot with horizontal legends
  #p4 <- p4 + theme(legend.position = "bottom") #+
     # guides(fill = guide_colorbar(barwidth = 5, barheight = 0.5, title.position = "top"))

  # Display final plot
  p3
}



# ------------------------------
# Example usage
# ------------------------------
#tree_file <- "synechococcus_mappedWH8101.astral4.mad.dnd"
tree_file <- "synechococcus_mappedWH8101.bppconsense.nw"
csv_file <- "synechococcus_temp_cats.csv"

input <- map_input(tree_file, csv_file)
heatmap_data <- prepare_heatmap_data(input$tree, input$categories)
plot <- create_plot(input$tree, heatmap_data)
print(plot)



