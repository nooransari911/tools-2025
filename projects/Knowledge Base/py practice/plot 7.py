import graphviz
import os
import html

# --- Configuration ---
output_filename = 'electromagnetics_large_text_flowchart'
output_format = 'png' # 'png', 'pdf', 'svg'

# Colors (Simplified Professional Palette)
node_color = '#005A9C'   # Consistent professional blue for all nodes
color_bg = '#FFFFFF'     # White background
color_arrow = '#555555'  # Darker grey for arrows
font_color = 'white'     # White text for contrast on blue background
font_name = 'Arial'      # Widely available sans-serif font

# Node dimensions (Adjust if text wrapping becomes an issue with large font)
node_width = '5.0' # Wider to accommodate larger text on one line
node_height = '0.8' # Can be shorter if text fits on fewer lines

# --- Create a Directed Graph ---
dot = graphviz.Digraph(comment='Large Text Electromagnetics Learning Path', engine='dot', format=output_format)
dot.attr(rankdir='TB', bgcolor=color_bg, nodesep='0.8', ranksep='0.8') # Increased ranksep slightly

# --- Define Node Styles (using HTML-like labels for formatting) ---

# Helper function to create the HTML label structure - Phase # and Title on one line
def create_html_label(phase_num, title_text, font_color, font_name):
    # Escape special HTML characters like '&'
    safe_title_text = html.escape(title_text)
    # Combine Phase Num (bold) and Title on one line
    label_line = f'<B>Phase {phase_num}:</B> {safe_title_text}'

    # Using larger POINT-SIZE
    # Wrapping TD in TR just for structure, could be single TD if preferred
    return f'''<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="12">
                 <TR><TD ALIGN="CENTER" VALIGN="MIDDLE">
                   <FONT FACE="{font_name}" COLOR="{font_color}" POINT-SIZE="16">{label_line}</FONT>
                 </TD></TR>
               </TABLE>>'''

# Define Nodes with consistent style
# Note: Explicitly setting fontname/color here is less critical due to HTML override,
# but can be good practice.
common_node_attrs = {
    'shape': 'box',
    'style': 'filled,rounded',
    'fillcolor': node_color,
    'fontname': font_name,
    'fontcolor': font_color, # Primarily for Graphviz internal use
    'width': node_width,
    'height': node_height,
    'fixedsize': 'true'
}

dot.node('phase1',
         label=create_html_label(1, 'Foundational Electromagnetic Concepts', font_color, font_name),
         **common_node_attrs)

dot.node('phase2',
         label=create_html_label(2, 'Wave Propagation & Transmission Lines', font_color, font_name),
         **common_node_attrs)

dot.node('phase3',
         label=create_html_label(3, 'Antenna Fundamentals', font_color, font_name),
         **common_node_attrs)

dot.node('phase4',
         label=create_html_label(4, 'Introduction to AEDT & HFSS Simulation', font_color, font_name),
         **common_node_attrs)


# --- Define Edge Styles ---
dot.attr('edge', color=color_arrow, arrowhead='normal', penwidth='1.5')

# --- Define Edges (Connections) ---
dot.edge('phase1', 'phase2')
dot.edge('phase2', 'phase3')
dot.edge('phase3', 'phase4')

# --- Render and Save ---
try:
    # Ensure Graphviz bin is in PATH if not added during install (example for Windows)
    # if "GRAPHVIZ_DOT" not in os.environ:
       # os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin' # Adjust path if needed

    dot.render(output_filename, view=False, cleanup=True)
    print(f"Large text flowchart successfully generated: {output_filename}.{output_format}")
except Exception as e:
    print(f"Error generating flowchart: {e}")
    print("Please ensure Graphviz is installed and its 'bin' directory is in your system's PATH.")
    print("Check font availability (e.g., Arial).")
    print("Download Graphviz from: https://graphviz.org/download/")
