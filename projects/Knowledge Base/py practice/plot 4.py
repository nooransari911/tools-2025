import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text # Helps prevent label overlap
import pandas as pd

# --- Data Preparation ---
# Based on the quantification table above
risk_data = [
    {'Risk': 'Lower Than Expected Utilization', 'Likelihood': 3, 'Impact': 3, 'Category': 'Market'},
    {'Risk': 'Inability to Service Debt', 'Likelihood': 2, 'Impact': 3, 'Category': 'Financial'},
    {'Risk': 'Construction Delays/Overruns', 'Likelihood': 2, 'Impact': 3, 'Category': 'Construction'},
    {'Risk': 'Permit/Approval Issues', 'Likelihood': 2, 'Impact': 3, 'Category': 'Construction'},
    {'Risk': 'High Operating Costs', 'Likelihood': 3, 'Impact': 2, 'Category': 'Financial'},
    {'Risk': 'Safety Incidents', 'Likelihood': 1, 'Impact': 3, 'Category': 'Operational'}, # Added from 6.2
    {'Risk': 'Intense Competition', 'Likelihood': 3, 'Impact': 2, 'Category': 'Market'},    # Added from 6.2
]

# Create a DataFrame
df = pd.DataFrame(risk_data)

# Calculate Risk Score for coloring/sizing (optional but informative)
df['Risk_Score'] = df['Likelihood'] * df['Impact']

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 8))

# Define score labels
score_labels = {1: 'Low', 2: 'Medium', 3: 'High'}
ticks = list(score_labels.keys())

# Define colors for risk levels based on score (example)
# Green (Low: 1-3), Yellow (Medium: 4-5), Orange (High: 6), Red (Very High: 7-9)
def get_color(score):
    if score <= 3: return 'green'
    if score <= 5: return 'gold' # Changed from yellow for better visibility
    if score == 6: return 'darkorange'
    else: return 'red'

colors = [get_color(score) for score in df['Risk_Score']]

# Scatter plot - size can also represent score or be fixed
scatter = ax.scatter(
    df['Likelihood'],
    df['Impact'],
    s=df['Risk_Score'] * 50,  # Size proportional to risk score (adjust multiplier as needed)
    c=colors,                # Color based on risk score
    alpha=0.7                # Transparency
)

# --- Customize Appearance ---

# Add Risk Matrix grid lines / background colors (optional)
ax.axhline(1.5, color='grey', linestyle='--', lw=0.5)
ax.axhline(2.5, color='grey', linestyle='--', lw=0.5)
ax.axvline(1.5, color='grey', linestyle='--', lw=0.5)
ax.axvline(2.5, color='grey', linestyle='--', lw=0.5)

# Fill background areas (optional, can make it busy)
# ax.fill_between([0.5, 1.5], 0.5, 1.5, color='green', alpha=0.1) # Low-Low
# ax.fill_between([1.5, 3.5], 2.5, 3.5, color='red', alpha=0.1)   # High-High, etc.

# Set axis limits and labels
ax.set_xlabel("Likelihood", fontsize=12)
ax.set_ylabel("Impact", fontsize=12)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels([score_labels[t] for t in ticks])
ax.set_yticklabels([score_labels[t] for t in ticks])
ax.set_xlim(0.5, 3.5)
ax.set_ylim(0.5, 3.5)

# Add Title
ax.set_title("Project Risk Matrix (Quantitative Assessment)", fontsize=14, pad=15)

# Add text labels for each point, adjusting for overlap
texts = []
for i, row in df.iterrows():
    # Add newline for longer labels if needed (simple example)
    label = row['Risk'].replace('/', '/\n')
    texts.append(ax.text(row['Likelihood'], row['Impact'], label, fontsize=8, ha='center', va='bottom'))

# Use adjust_text to prevent labels from overlapping
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))

# Add a simple legend for colors (manual approach)
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Score 1-3 (Low)', markersize=8, markerfacecolor='green'),
    plt.Line2D([0], [0], marker='o', color='w', label='Score 4-5 (Medium)', markersize=8, markerfacecolor='gold'),
    plt.Line2D([0], [0], marker='o', color='w', label='Score 6 (High)', markersize=8, markerfacecolor='darkorange'),
    plt.Line2D([0], [0], marker='o', color='w', label='Score 7-9 (Very High)', markersize=8, markerfacecolor='red')
]
ax.legend(handles=legend_elements, title="Risk Score", loc='upper left', bbox_to_anchor=(1.02, 1))


# Improve layout
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust rect to make space for legend outside

# Display the plot
plt.show()
