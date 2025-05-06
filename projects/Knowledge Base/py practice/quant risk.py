import graphviz
import os

# --- Configuration ---
output_filename = 'risk_management_cycle'
output_format = 'png'  # Or 'pdf', 'svg'
view_chart_after_creation = True

# --- Create the Graph ---
dot = graphviz.Digraph(
    'RiskManagementCycle',
    comment='Risk Management Process Cycle Diagram',
    graph_attr={
        'rankdir': 'TB',          # Layout direction (Top to Bottom)
        'splines': 'curved',      # Use curved edges, can look good for cycles
        'overlap': 'false',       # Try to prevent node overlap
        'nodesep': '0.5',         # Separation between nodes on same rank
        'ranksep': '0.6',         # Separation between ranks
        'label': 'Risk Management Process Cycle', # Diagram Title
        'labelloc': 't',          # Position title at the top
        'fontsize': '14',         # Title font size
        'fontname': 'Arial'
    },
    node_attr={
        'shape': 'box',
        'style': 'rounded,filled',
        'fillcolor': '#e6f2ff',  # Light blue fill
        'color': '#004085',     # Darker blue border
        'fontname': 'Arial',
        'fontsize': '10'
    },
    edge_attr={
        'color': '#4d4d4d',     # Dark grey arrows
        'arrowsize': '0.8',
        'fontname': 'Arial',
        'fontsize': '9'
    }
)

# --- Define the Nodes (Stages) ---
dot.node('ID', '1. Risk Identification\n(Identify & Categorize Risks)')
dot.node('ASSESS', '2. Risk Assessment\n(Likelihood & Impact Analysis)')
dot.node('MITIGATE', '3. Mitigation Planning\n(Develop Response Strategies)')
dot.node('MONITOR', '4. Monitoring & Review\n(Track Risks & Plan Effectiveness)')

# --- Define the Edges (Flow) ---
# Sequential flow
dot.edge('ID', 'ASSESS', label=' Assess ') # Label edges for clarity
dot.edge('ASSESS', 'MITIGATE', label=' Plan Response ')
dot.edge('MITIGATE', 'MONITOR', label=' Implement & Track ')

# Feedback loop to complete the cycle
dot.edge('MONITOR', 'ID', label=' Feedback / New Risks ', constraint='true') # Ensure this edge influences layout

# --- Render and Save ---
try:
    dot.render(output_filename, format=output_format, view=view_chart_after_creation, cleanup=True)
    print(f"Risk Management Cycle diagram saved as '{output_filename}.{output_format}'")
    if view_chart_after_creation:
        print("Attempting to open the chart...")
except graphviz.exceptions.ExecutableNotFound:
    print("\n--- ERROR ---")
    print("Graphviz executable not found. Please ensure Graphviz is installed")
    print("AND that its 'bin' directory is in your system's PATH environment variable.")
    print("Download Graphviz from: https://graphviz.org/download/")
except Exception as e:
    print(f"\n--- An error occurred during rendering: ---")
    print(e)
