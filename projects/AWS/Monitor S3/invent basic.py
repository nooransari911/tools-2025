import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# ... (Data loading and cleaning remain the same)
# DATA LOADING AND CLEANING
file_path = '/home/studio-lab-user/sagemaker-studiolab-notebooks/AWS/csv/2024-09-28.csv'  # Replace with your file path if needed
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    exit()



df['size'] = df['size'].fillna(0)
for col in ['is_latest', 'is_delete_marker']:
    df[col] = df[col].astype(str).str.upper().replace({'NAN': 'FALSE'})




# Aggregation based on 'storage_class'
grouped_df = df.groupby('storage_class').agg(
    total_size=('size', 'sum'),
    object_count=('key', 'count'),
    is_latest_count=('is_latest', lambda x: (x == 'TRUE').sum()),
    is_not_latest_count=('is_latest', lambda x: (x == 'FALSE').sum()),
    is_not_delete_count=('is_delete_marker', lambda x: (x == 'FALSE').sum()) # Correcting is_delete aggregation
).reset_index()

# Dividing total size by 1 billion
grouped_df['total_size'] = grouped_df['total_size'] / 1000000000



print("\n\nAgg df")
"""Prints a pandas DataFrame with aligned columns."""
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(grouped_df.to_string(index=False)) # index=False so that index numbers do not get displayed
print("\n\n\n\n")


# Set dark theme and colors
sns.set(style="darkgrid")
colors = sns.color_palette("Set2")



# Plotting all metrics as lines
# Plotting all metrics as lines (Corrected Plotting Logic)
fig, ax1 = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor('#333333')
ax1.set_facecolor('#333333')


ax1.set_xlabel("Storage Class", color='white')
ax1.set_ylabel("Size (GB)", color='white')
ax1.tick_params(axis='y', labelcolor='white')
#ax1.set_xticklabels(grouped_df['storage_class'], color='white')  # Set x-tick labels to white


ax2 = ax1.twinx()
ax2.set_ylabel("Counts", color='white')
ax2.tick_params(axis='y', labelcolor='white')




handles, labels = [],[]
line_styles = ['o', 's', '^', 'x', 'D', 'P', 'h', 'v', '<', '>', '1', '2', '3', '4', '8', 'p', '*', '+', '|', '_']    # Different marker styles for lines
metrics = ['total_size', 'object_count', 'is_latest_count', 'is_not_latest_count', 'is_not_delete_count']
x_positions = np.arange(len(metrics))  # Evenly spaced x-positions for each metric





for metric, color, style in zip(metrics, colors, line_styles):
    ax = ax1 if metric == 'total_size' else ax2  # Choose appropriate axis

    # Plot the line (fix: no unpacking needed, get the artist directly)
    plot_result = sns.lineplot(x='storage_class', y=metric, data=grouped_df, color=color, ax=ax, marker=style[0], linestyle=style[1:], legend=False)

    # Extract the line artist from the plot_result
    line = plot_result.get_lines()[0]  # Get the Line2D artist object


    handles.append(line)  # Append the line artist to handles
    labels.append(metric.replace("_", " ").title())



# Combining the legends (only one axis now)



ax1.legend(handles, labels, loc='upper left')

# Remove grid lines
ax1.grid(False)  # Remove grid from primary y-axis
ax2.grid(False)  # Remove grid from secondary y-axis





plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()
