import matplotlib.pyplot as plt

# Data from the table
labels = [
    'Land Acquisition/Leasehold',
    'Construction & Civil Works',
    'Core Badminton Equipment',
    'Facility Fit-out & Other Equip.',
    'Pre-operative Expenses',
    'Contingency Reserve'
]
sizes = [
    40000000,  # Land
    50000000,  # Construction
    5000000,   # Core Equipment
    10000000,  # Fit-out
    7500000,   # Pre-operative
    7500000    # Contingency
]
total_cost = 120000000

# Optional: Explode the largest slice (Construction)
explode = (0, 0.1, 0, 0, 0, 0)

# Define colors (optional)
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

# Create the pie chart
fig1, ax1 = plt.subplots(figsize=(8, 8)) # Make figure a bit larger
ax1.pie(sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%', # Format percentages
        shadow=True,
        startangle=140) # Start angle rotates the chart for better label placement

# Equal aspect ratio ensures that pie is drawn as a circle.
ax1.axis('equal')

# Add title
plt.title(f"Project Cost Breakdown (Total: ₹{total_cost:,.0f})", pad=20)

# Improve layout to prevent label overlap if possible
plt.tight_layout()

# Display the chart
plt.show()
