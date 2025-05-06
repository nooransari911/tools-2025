import graphviz
import os

# Optional: Set environment variable to handle potential character encoding issues (like °)
# os.environ["PYTHONIOENCODING"] = "utf-8" # Usually not needed if system default is UTF-8

# 1. Create a new directed graph instance
#    'TB' = Top-to-Bottom layout
#    Removed 'splines=ortho' to allow for smoother/curved loops
#    'nodesep' and 'ranksep' control spacing between nodes and ranks (levels)
dot = graphviz.Digraph(
    'TemperatureControlProcess',
    comment='Flowchart for Temperature Control System',
    graph_attr={'rankdir': 'TB', 'nodesep': '0.6', 'ranksep': '0.8'} # Removed splines=ortho
)

# 2. Define global node attributes for consistent styling
dot.attr('node',
         shape='box',              # Default shape for process steps
         style='filled',
         fillcolor='lightblue',    # Light blue fill for process steps
         fontname='Helvetica',     # Professional font
         fontsize='11'
)

# 3. Define global edge attributes
dot.attr('edge',
         fontname='Helvetica',
         fontsize='10'
)

# 4. Define the nodes with specific labels and shapes where needed
#    Terminators (Start/End) use ellipse shape
#    Decision uses diamond shape
dot.node('START', 'Start', shape='ellipse', fillcolor='lightgreen')
dot.node('SYS_START', 'Start the System')
dot.node('CONFIG_SENS', 'Configure Temp Sensor')
dot.node('COIL_ON', 'Turn ON Heating Coil')
dot.node('CHECK_TEMP', 'Temp > 120°C?', shape='diamond', fillcolor='lightyellow') # Decision node
dot.node('COIL_OFF', 'Turn OFF Heating Coil')
dot.node('END', 'End', shape='ellipse', fillcolor='lightcoral')


# 5. Define the edges (connections) between the nodes to represent the flow
dot.edge('START', 'SYS_START')
dot.edge('SYS_START', 'CONFIG_SENS')
dot.edge('CONFIG_SENS', 'COIL_ON')
dot.edge('COIL_ON', 'CHECK_TEMP')

# Decision branches from CHECK_TEMP node
# Label edges originating from a decision node
# The ' No ' edge loops back to the input of the check, representing waiting/re-checking
# Using default splines should make this loop look smoother.
# Added 'taillabel' and 'headlabel' for better positioning relative to start/end points
# 'lp' (label position) can also help center the label on the edge path.
dot.edge('CHECK_TEMP', 'CHECK_TEMP', label=' No ') # Loop represents waiting
dot.edge('CHECK_TEMP', 'COIL_OFF', label=' Yes ')

dot.edge('COIL_OFF', 'END')

# 6. Render the flowchart
#    filename: Name of the output files (e.g., flowchart.gv, flowchart.gv.png)
#    format: Output format (png, pdf, svg, etc.)
#    view=True: Automatically opens the generated flowchart image
#    cleanup=True: Removes the intermediate .gv source file after rendering
try:
    # Use UTF-8 explicitly during rendering if needed
    dot.encoding = 'utf-8'
    output_filename = 'temperature_control_flowchart_v2' # Changed filename to avoid overwriting
    dot.render(output_filename, view=True, format='png', cleanup=True)
    print(f"Flowchart '{output_filename}.png' created and opened successfully.")
    print(f"Graphviz source saved to '{output_filename}.gv' (before cleanup).")
except graphviz.backend.execute.ExecutableNotFound:
    print("Error: Graphviz executable not found.")
    print("Please install Graphviz (from https://graphviz.org/download/)")
    print("and ensure its 'bin' directory is in your system's PATH.")
except Exception as e:
    print(f"An error occurred during flowchart generation: {e}")

# You can also print the DOT source code directly
# print("\nGenerated DOT source code:")
# print(dot.source)
