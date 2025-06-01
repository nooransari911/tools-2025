import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Data Preparation ---
# Data extracted from the cash flow statement (Section 5.1)
data = {
    'Year': [1, 2, 3, 4, 5],
    'Net Cash from Operations (A)': [-35.00, -28.00, -17.00, -11.00, -5.00],
    'Net Cash from Investing (B)': [0.00, -10.00, -10.00, -10.00, -10.00],
    'Net Cash from Financing (C)': [0.00, 0.00, -72.00, -72.00, -72.00],
    'Net Change in Cash (A+B+C)': [-35.00, -38.00, -99.00, -93.00, -87.00]
}

df = pd.DataFrame(data)
df.set_index('Year', inplace=True)

# Select only the component columns for plotting
plot_df = df[['Net Cash from Operations (A)',
              'Net Cash from Investing (B)',
              'Net Cash from Financing (C)']]

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 6)) # Slightly adjusted size

# Plotting stacked bars
plot_df.plot(kind='bar', stacked=True, ax=ax, width=0.7,
             color=['#1f77b4', '#ff7f0e', '#2ca02c']) # Using default matplotlib colors explicitly

# --- Chart Enhancements ---
ax.set_title('Projected Net Cash Flow by Activity (Years 1-5)', fontsize=16, pad=20)
ax.set_xlabel('Projection Year', fontsize=12)
ax.set_ylabel('Amount (INR Lakhs)', fontsize=12)

# Add a horizontal line at zero for clarity
ax.axhline(0, color='black', linewidth=0.8)

# Improve legend - *** MODIFIED HERE ***
ax.legend(title='Cash Flow Activity', loc='lower left', fontsize=10, title_fontsize=11)
# Removed bbox_to_anchor, changed loc to 'lower left'

# Add grid lines for better readability
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Rotate x-axis labels for better fit
plt.xticks(rotation=0)

# Removed bar labels as they would definitely clash with the legend now

plt.tight_layout() # Standard tight_layout should suffice now
plt.show()

# --- Interpretation ---
# (Interpretation remains the same as before)
print("\n--- Chart Interpretation ---")
print("The stacked bar chart visualizes the net cash flow from each activity per year:")
print("- Blue bars (Operations): Shows cash consumed by operations, improving but remaining negative in early years.")
print("- Orange bars (Investing): Shows minimal cash outflow for ongoing investments after Year 1.")
print("- Green bars (Financing): Shows zero net flow initially, then significant cash outflow from Year 3 onwards due to debt principal repayments.")
print("The total height of the stacked bar for each year represents the 'Net Change in Cash'.")
print("The predominantly negative stacks clearly illustrate the projected overall cash deficit each year, particularly after debt repayments begin, reinforcing the financial challenges highlighted in the proposal.")
