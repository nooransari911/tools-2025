import graphviz
import os

# Optional: Set environment variable to handle potential character encoding issues (like °)
# os.environ["PYTHONIOENCODING"] = "utf-8" # Usually not needed if system default is UTF-8

# 1. Create a new directed graph instance
dot = graphviz.Digraph(
    'TemperatureControlProcess_BW', # Changed graph name slightly for uniqueness
    comment='Flowchart for Temperature Control System (Black & White)',
    graph_attr={'rankdir': 'TB', 'nodesep': '0.6', 'ranksep': '0.8'}
)

# 2. Define global node attributes for consistent styling (BLACK & WHITE)
dot.attr('node',
         shape='box',              # Default shape for process steps
         style='filled',           # Ensure fill is applied
         fillcolor='white',        # White fill for all nodes
         color='black',            # Black border for all nodes
         fontcolor='black',        # Black text for all nodes
         fontname='Helvetica',     # Professional font
         fontsize='11'
)

# 3. Define global edge attributes (BLACK & WHITE)
dot.attr('edge',
         color='black',            # Black lines for all edges
         fontcolor='black',        # Black text for edge labels
         fontname='Helvetica',
         fontsize='10'
)

# 4. Define the nodes with specific labels and shapes where needed
#    Terminators (Start/End) use ellipse shape
#    Decision uses diamond shape
#    All fillcolors are now white, inheriting other B&W attributes from global settings.
dot.node('START', 'Start', shape='ellipse', fillcolor='white') # fillcolor explicitly white
dot.node('SYS_START', 'Start the System')
dot.node('CONFIG_SENS', 'Configure Temp Sensor')
dot.node('COIL_ON', 'Turn ON Heating Coil')
dot.node('CHECK_TEMP', 'Temp > 120°C?', shape='diamond', fillcolor='white') # fillcolor explicitly white
dot.node('COIL_OFF', 'Turn OFF Heating Coil')
dot.node('END', 'End', shape='ellipse', fillcolor='white') # fillcolor explicitly white


# 5. Define the edges (connections) between the nodes to represent the flow
dot.edge('START', 'SYS_START')
dot.edge('SYS_START', 'CONFIG_SENS')
dot.edge('CONFIG_SENS', 'COIL_ON')
dot.edge('COIL_ON', 'CHECK_TEMP')

# Decision branches from CHECK_TEMP node
dot.edge('CHECK_TEMP', 'CHECK_TEMP', label=' No ') # Loop represents waiting
dot.edge('CHECK_TEMP', 'COIL_OFF', label=' Yes ')

dot.edge('COIL_OFF', 'END')

# 6. Render the flowchart
try:
    dot.encoding = 'utf-8'
    output_filename = 'temperature_control_flowchart_bw' # New filename for B&W version
    dot.render(output_filename, view=True, format='png', cleanup=True)
    print(f"Flowchart '{output_filename}.png' created and opened successfully.")
    # print(f"Graphviz source saved to '{output_filename}.gv' (before cleanup).") # Usually removed by cleanup
except graphviz.backend.execute.ExecutableNotFound:
    print("Error: Graphviz executable not found.")
    print("Please install Graphviz (from https://graphviz.org/download/)")
    print("and ensure its 'bin' directory is in your system's PATH.")
except Exception as e:
    print(f"An error occurred during flowchart generation: {e}")

# You can also print the DOT source code directly
# print("\nGenerated DOT source code:")
# print(dot.source)
