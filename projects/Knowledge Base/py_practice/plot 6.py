import graphviz
import os

# Ensure Graphviz binaries are in the system PATH (especially important on Windows if not added during installation)
# You might need to adjust this path based on your Graphviz installation location
# Example for default Windows install location:
# os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

# --- Flowchart Configuration ---
output_filename = 'hfss_simulation_flowchart'
output_format = 'png' # Common formats: 'png', 'pdf', 'svg', 'jpg'
graph_title = 'HFSS Simulation Workflow for 5-Element Dipole Array'

# --- Create a Directed Graph (Flowchart) ---
# 'TB' means Top-to-Bottom layout
dot = graphviz.Digraph(comment=graph_title, engine='dot', format=output_format)
dot.attr(rankdir='TB', label=graph_title, fontsize='16', fontname='Helvetica', labelloc='t')
dot.attr('node', shape='box', style='filled,rounded', fillcolor='lightblue', fontname='Helvetica', fontsize='10')
dot.attr('edge', fontname='Helvetica', fontsize='9')

# --- Define Flowchart Nodes (Steps) ---
# Use concise node IDs and descriptive labels from the input text
dot.node('start', 'Start', shape='ellipse', style='filled', fillcolor='lightgrey')
dot.node('geom_def', 'Geometry Definition:\nConstruct 3D model of dipole elements\nand surrounding air/vacuum region.')
dot.node('mat_assign', 'Material Assignment:\nAssign properties (e.g., copper for dipoles,\nvacuum for surrounding space).')
dot.node('bc_apply', 'Boundary Conditions:\nApply conditions (e.g., \'Radiation\' boundary\non air box faces for free space simulation).')
dot.node('excitations', 'Excitations/Sources:\nDefine input sources (e.g., \'Lumped Ports\'\nat the center gap of each dipole).')
dot.node('analysis_setup', 'Analysis Setup:\nConfigure parameters (Solution Frequency: 5.5 GHz,\nFrequency Sweep: 4-7 GHz, Mesh settings).')
dot.node('solve', 'Solving:\nLaunch HFSS solver (FEM computation\nof E/M fields based on Maxwell\'s equations).')
dot.node('post_process', 'Post-Processing:\nAnalyze results (S11 vs. frequency plots,\nFar-field radiation patterns, Peak Directivity).')
dot.node('end', 'End', shape='ellipse', style='filled', fillcolor='lightgrey')

# --- Define Flowchart Edges (Connections) ---
dot.edge('start', 'geom_def')
dot.edge('geom_def', 'mat_assign')
dot.edge('mat_assign', 'bc_apply')
dot.edge('bc_apply', 'excitations')
dot.edge('excitations', 'analysis_setup')
dot.edge('analysis_setup', 'solve')
dot.edge('solve', 'post_process')
dot.edge('post_process', 'end')

# --- Render and Save the Flowchart ---
try:
    # The render function saves the graph and source file.
    # `view=True` attempts to open the generated file automatically.
    # `cleanup=True` removes the intermediate '.gv' source file.
    dot.render(output_filename, view=False, cleanup=True)
    print(f"Flowchart successfully generated: {output_filename}.{output_format}")
    # You can manually change view=True if you want it to open automatically
    # Note: Automatic view depends on having a default application associated with the output format.
except Exception as e:
    print(f"Error generating flowchart: {e}")
    print("Please ensure Graphviz is installed and its 'bin' directory is in your system's PATH.")
    print("Download from: https://graphviz.org/download/")
