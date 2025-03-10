import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

folder_path = '2025dbres'  
csv_files = [f for f in os.listdir(folder_path) if f.endswith('params.csv')]
all_data = []

for file in csv_files:
    # Extract category number (e.g., cat1, cat2, etc.)
    name = file.split('_')
    category = name[2] + '_' + name[3]
    print(category)
    
    df = pd.read_csv(os.path.join(folder_path, file))
    df['category'] = category
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
print(data)

# Melt the DataFrame to long format for easy plotting
data_long = data.melt(id_vars=['category'], value_vars=['S_d', 'S_b', 'b', 'p_b', 'eps', 'alpha'],
                      var_name='Parameter', value_name='Value')

# Use absolute values for the 'Value' column
data_long['Value'] = data_long['Value'].abs()

# Create a color palette for pairs
unique_categories = sorted(data['category'].unique())  # Sort categories alphabetically
palette = sns.color_palette("tab10", len(unique_categories)) #Paired

# Map categories to colors
category_colors = {cat: palette[i] for i, cat in enumerate(unique_categories)}

# Plot using Seaborn
plt.figure(figsize=(12, 8))
sns.barplot(data=data_long, x='Parameter', y='Value', hue='category', dodge=True,
            palette=category_colors, hue_order=unique_categories)

# Set the y-axis to log scale
plt.yscale('log')

# Add a title and labels
plt.title('Log-Scale Parameter Values for Different Categories', fontsize=16)
plt.xlabel('Parameter', fontsize=12)
plt.ylabel('Log(Value)', fontsize=12)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.tight_layout()
plt.show()
