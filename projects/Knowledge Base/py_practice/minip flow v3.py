import graphviz
import os

# 1. Create a new directed graph instance
dot = graphviz.Digraph(
    'TemperatureControlProcess_BW_3Turn',
    comment='Flowchart for Temperature Control System (BW, 3-Turn Ortho Arrow)',
    graph_attr={
        'rankdir': 'TB',
        'nodesep': '0.6',
        'ranksep': '0.8',
        'splines': 'ortho'  # Ensure orthogonal lines
    }
)

# 2. Define global node attributes (BLACK & WHITE)
dot.attr('node',
         shape='box',
         style='filled',
         fillcolor='white',
         color='black',
         fontcolor='black',
         fontname='Helvetica',
         fontsize='11'
)

# 3. Define global edge attributes (BLACK & WHITE)
dot.attr('edge',
         color='black',
         fontcolor='black',
         fontname='Helvetica',
         fontsize='10'
)

# 4. Define the nodes
dot.node('START', 'Start', shape='ellipse', fillcolor='white')
dot.node('SYS_START', 'Start the System')
dot.node('CONFIG_SENS', 'Configure Temp Sensor')
dot.node('COIL_ON', 'Turn ON Heating Coil')
dot.node('CHECK_TEMP', 'Temp > 120°C?', shape='diamond', fillcolor='white')
dot.node('COIL_OFF', 'Turn OFF Heating Coil')
dot.node('END', 'End', shape='ellipse', fillcolor='white')

# Define an invisible node to guide the "No" path
# Make it very small and without a label. 'point' shape is good.
# We'll place it logically to the left of the main flow and between the ranks
# of CHECK_TEMP and CONFIG_SENS.
dot.node('INV_NO_POINT', shape='point', width='0.01', height='0.01', label='')


# 5. Define the edges
dot.edge('START', 'SYS_START')
dot.edge('SYS_START', 'CONFIG_SENS')
dot.edge('CONFIG_SENS', 'COIL_ON')
dot.edge('COIL_ON', 'CHECK_TEMP')

# Decision branches from CHECK_TEMP node

# "Yes" branch - straightforward
dot.edge('CHECK_TEMP', 'COIL_OFF', label=' Yes ')

# "No" branch - routed via the invisible node for 3 turns
# 1. From CHECK_TEMP's west side to the invisible point's south side.
#    This makes the invisible point sit to the left and slightly above CHECK_TEMP.
#    The `constraint=false` helps prevent this backward edge from messing with ranks too much.
dot.edge('CHECK_TEMP:w', 'INV_NO_POINT:s', label=' No ', constraint='false')

# 2. From the invisible point's north side to CONFIG_SENS's east side.
#    This creates the upward and then rightward movement.
dot.edge('INV_NO_POINT:n', 'CONFIG_SENS:e')


dot.edge('COIL_OFF', 'END')

# 6. Render the flowchart
try:
    dot.encoding = 'utf-8'
    output_filename = 'temperature_control_flowchart_bw_3turn'
    dot.render(output_filename, view=True, format='png', cleanup=True)
    print(f"Flowchart '{output_filename}.png' created and opened successfully.")
except graphviz.backend.execute.ExecutableNotFound:
    print("Error: Graphviz executable not found.")
    print("Please install Graphviz (from https://graphviz.org/download/)")
    print("and ensure its 'bin' directory is in your system's PATH.")
except Exception as e:
    print(f"An error occurred during flowchart generation: {e}")
