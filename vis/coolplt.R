# Required libraries
library(ape)
library(ggtree)
library(dplyr)
library(ggplot2)
library(tidyr)
library(ggnewscale)
library(RColorBrewer)
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


  # Bin continuous variables
  categories <- categories %>%
    mutate(
      lat_bin = cut(Isolation_latitude_N, breaks = seq(-180, 180, by = 30), include.lowest = TRUE),
      lon_bin = cut(Isolation_longitude_E, breaks = seq(-180, 180, by = 30), include.lowest = TRUE),
      temp_bin = cut(isolation_temperature, breaks = seq(5, 30, by = 5), include.lowest = TRUE)
    )

  # Prepare long format data for heatmap
  heatmap_data <- categories %>%
    select(strain_name, clade_species, isolation_ocean, lat_bin, lon_bin, temp_bin) %>%
    pivot_longer(-strain_name, names_to = "property", values_to = "value") %>%
    filter(!is.na(value))

  if (nrow(heatmap_data) == 0) {
    stop("No valid data found for heatmap plotting. Check the CSV input.")
  }

  heatmap_data
}

# ------------------------------
# Function: create_plot
# ------------------------------
create_plot <- function(tree, heatmap_data, output_csv = "heatmap_wide.csv") {
  # Plot the phylogenetic tree
  p <- ggtree(tree) + geom_tiplab(size = 3)

  # Reshape heatmap data to wide format
  heatmap_wide <- heatmap_data %>% pivot_wider(names_from = property, values_from = value)

  # Write the heatmap_wide data frame to a CSV file
  write.csv(heatmap_wide, file = output_csv, row.names = FALSE)
  
  # Identify heatmap columns
  heatmap_columns <- setdiff(colnames(heatmap_wide), "strain_name")
  if (length(heatmap_columns) == 0) {
    stop("No columns available for heatmap plotting.")
  }

  # Ensure columns are factors for discrete properties
  discrete_properties <- c("clade_species", "isolation_ocean")
  continuous_properties <- setdiff(heatmap_columns, discrete_properties)

  heatmap_wide[discrete_properties] <- lapply(heatmap_wide[discrete_properties], factor)
  heatmap_wide[continuous_properties] <- lapply(heatmap_wide[continuous_properties], as.character)  # Keep them as factors for binning

  # Plot first heatmap (discrete properties)
  p <- gheatmap(p, heatmap_wide[, discrete_properties, drop = FALSE], offset = 0.05, width = 0.6,
                colnames_position = "top", font.size = 3, hjust = 0) +
    scale_fill_manual(values = RColorBrewer::brewer.pal(8, "Set2"), na.value = "grey90") +
    theme(legend.position = "bottom") +
    ggnewscale::new_scale_fill()

  # Add second heatmap (continuous properties) with a different scale
  p <- gheatmap(p, heatmap_wide[, continuous_properties, drop = FALSE], offset = 0.05, width = 0.6,
                colnames_position = "top", font.size = 3, hjust = 0) +
    scale_fill_gradient(low = "blue", high = "red", na.value = "grey90") +
    theme(legend.position = "bottom")

  p
}



# ------------------------------
# Example usage
# ------------------------------
tree_file <- "synechococcus_mappedWH8101.astral4.mad.dnd"
csv_file <- "synechococcus_temp_cats.csv"

input <- map_input(tree_file, csv_file)
heatmap_data <- prepare_heatmap_data(input$tree, input$categories)
plot <- create_plot(input$tree, heatmap_data)
print(plot)
