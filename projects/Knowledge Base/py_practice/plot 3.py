import matplotlib.pyplot as plt
import matplotlib.ticker as mticker # Although not used for formatting slices here, good practice to import

# --- Data ---
labels = ['Equity - Promoter\'s Capital', 'Equity - Private Equity', 'Debt - Term Loan']
# Values in base INR units
sizes_inr = [28800000, 19200000, 72000000]
total_funding_inr = 120000000

# --- Create Formatting Function ---
# This function converts the calculated percentage back to the absolute value in Crores
def value_in_crores(pct):
    absolute_value = total_funding_inr * pct / 100
    value_cr = absolute_value / 1_00_00_000 # 1 Crore = 1,00,00,000
    # Format the string to show "₹X.XX Cr"
    return f'₹{value_cr:.2f} Cr'

# --- Plotting ---
fig, ax = plt.subplots(figsize=(8, 8)) # Make figure slightly larger for labels

# Define colors (optional, but improves appearance)
# Colors chosen to loosely represent equity (blues) and debt (reddish)
colors = ['#66b3ff', '#99ccff', '#ff9999']

# Explode the largest slice (Debt - Term Loan) slightly for emphasis (optional)
explode = (0, 0, 0.1)

wedges, texts, autotexts = ax.pie(
    sizes_inr,
    labels=labels,
    autopct=value_in_crores, # Use the custom function here!
    startangle=90,          # Rotates the start of the first slice
    colors=colors,
    explode=explode,
    pctdistance=0.8,         # Distance of the value text from the center
    labeldistance=1.05       # Distance of the category labels from the center
)

# --- Customize Appearance ---

# Improve text properties (optional)
plt.setp(autotexts, size=10, weight="bold", color="black")
plt.setp(texts, size=9)

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.axis('equal')

# Add Title
ax.set_title(f"Source of Funds (Total: ₹{total_funding_inr / 1_00_00_000:.2f} Cr)", pad=20)

# Improve layout slightly if labels overlap
plt.tight_layout()

# Display the chart
plt.show()
