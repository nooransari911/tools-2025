import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# --- Data Preparation ---
# Combine the data from the tables

# Data extracted manually (ensure accuracy)
years_list = [1, 2, 3, 4, 5]
revenue_inr = [18000000, 19000000, 20500000, 21500000, 22500000]
ebitda_inr = [4000000, 4200000, 4800000, 4900000, 5000000]
pbt_inr = [-6000000, -5300000, -4200000, -3600000, -3000000]

# You could also use pandas to structure this if preferred
data = {
    'Year': years_list,
    'Revenue': revenue_inr,
    'EBITDA': ebitda_inr,
    'PBT': pbt_inr
}
df = pd.DataFrame(data)

# --- Plotting ---

# Define a formatter function for the Y-axis (display in Millions)
def millions_formatter(x, pos):
    'The two args are the value and tick position'
    if x == 0:
        return '₹0'
    else:
        return f'₹{x/1_000_000:,.0f}M' # Format as integer millions

formatter = mticker.FuncFormatter(millions_formatter)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6)) # Adjust figure size as needed

# Plot the data lines
ax.plot(df['Year'], df['Revenue'], label='Revenue', marker='o', linewidth=2)
ax.plot(df['Year'], df['EBITDA'], label='EBITDA', marker='s', linewidth=2)
ax.plot(df['Year'], df['PBT'], label='Profit Before Tax (PBT)', marker='^', linewidth=2, color='red')

# Add a horizontal line at zero for reference
ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)

# --- Customize Appearance ---

# Add labels and title
ax.set_xlabel("Projection Year")
ax.set_ylabel("Amount (INR)")
ax.set_title("Projected Profit & Loss Summary (5 Years)", fontsize=14, pad=15)

# Apply the custom formatter to the Y-axis
ax.yaxis.set_major_formatter(formatter)

# Set X-axis ticks to show every year clearly
ax.set_xticks(df['Year'])

# Add a legend
ax.legend()

# Add grid lines for better readability
ax.grid(True, linestyle=':', alpha=0.6)

# Improve layout
plt.tight_layout()

# Display the plot
plt.show()
