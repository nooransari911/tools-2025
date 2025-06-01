import graphviz
import os

# Optional: Ensure Graphviz executables are in the system's PATH
# os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin' # Example for Windows

# --- Configuration ---
output_filename = 'badminton_centre_org_chart_v5' # New filename
output_format = 'png'
view_chart_after_creation = True

# Define colors
colors = {
    'board': '#f8d7da',
    'director': '#cce5ff',
    'manager': '#d4edda',
    'staff': '#fff3cd',
    'dept_bg': '#f2f2f2'
}

# --- Create the Graph ---
dot = graphviz.Digraph(
    'OrganizationalChart',
    comment='[Location] Badminton Centre Pvt. Ltd. Org Chart',
    graph_attr={
        'rankdir': 'TB',
        'splines': 'ortho', # Use orthogonal lines for cleaner look
        'nodesep': '0.6',   # Horizontal separation
        'ranksep': '0.8',   # << ADJUSTED >> Vertical separation between ranks
        'bgcolor': 'white'
    },
    node_attr={
        'shape': 'box',
        'style': 'filled',
        'fontname': 'Arial',
        'fontsize': '10',
        'margin': '0.15,0.1'
    },
    edge_attr={
        'fontname': 'Arial',
        'fontsize': '9',
        'arrowsize': '0.7',
        'color': 'black' # Ensure edges are visible
    }
)

# --- Define Nodes and Structure ---

# Top Level
dot.node('board', 'Board / Investors', fillcolor=colors['board'])

# Facility Director
dot.node('director', 'Facility Director', fillcolor=colors['director'])
dot.edge('board', 'director')

# === Invisible Node for "Departments" Label ===
dot.node('dept_label_node', 'Departments', shape='plain', fontsize='12', fontname='Arial')

# Edges to establish ranking for the Departments label node
dot.edge('director', 'dept_label_node', style='invis') # Invisible edge for ranking

# Cluster for Department Managers (still visually grouped)
with dot.subgraph(name='cluster_departments') as dept_cluster:
    # << REMOVED label attribute from cluster >>
    dept_cluster.attr(
        style='filled',
        color=colors['dept_bg'], # Background color only
        margin='15'
    )
    # Managers
    dept_cluster.node('ops_mgr', 'Operations Manager', fillcolor=colors['manager'])
    dept_cluster.node('sales_mgr', 'Sales & Marketing Manager', fillcolor=colors['manager'])
    dept_cluster.node('head_coach', 'Head Coach', fillcolor=colors['manager'])
    dept_cluster.node('fin_admin_mgr', 'Finance & Admin Manager', fillcolor=colors['manager'])
    dept_cluster.graph_attr.update(rank='same') # Keep managers aligned

# Edges from Director to Managers (visible reporting lines)
# These should bypass the label node visually due to 'ortho' splines
dot.edge('director', 'ops_mgr')
dot.edge('director', 'sales_mgr')
dot.edge('director', 'head_coach')
dot.edge('director', 'fin_admin_mgr')

# === Invisible Node for "Teams / Operational Roles" Label ===
dot.node('team_label_node', 'Teams / Operational Roles', shape='plain', fontsize='12', fontname='Arial')

# Invisible edges to establish ranking for the Teams label node
# Connect from label node *above* to this label node
dot.edge('dept_label_node', 'team_label_node', style='invis')
# Also connect from at least one manager to this label node
dot.edge('ops_mgr', 'team_label_node', style='invis') # From one manager node
dot.edge('sales_mgr', 'team_label_node', style='invis')
dot.edge('head_coach', 'team_label_node', style='invis')
dot.edge('fin_admin_mgr', 'team_label_node', style='invis')


# Cluster for Teams (still visually grouped)
with dot.subgraph(name='cluster_teams') as team_cluster:
     # << REMOVED label attribute from cluster >>
    team_cluster.attr(
        style='filled',
        color=colors['dept_bg'], # Background color only
        margin='15'
    )

    # Nested Clusters for specific teams (labels now inside *these* clusters are okay)
    cluster_common_attrs = {
        'style': 'dotted', 'color': 'grey', 'fontname': 'Arial',
        'fontsize': '10', 'labelloc': 't', 'labeljust': 'l', 'margin': '8'
    }

    # Operations Team
    with team_cluster.subgraph(name='cluster_ops_team') as ops_team:
        ops_team.attr(label='Operations', **cluster_common_attrs)
        ops_team.node('maint_staff', 'Maintenance / \nHousekeeping Staff', fillcolor=colors['staff'])
        # Invisible edge for ranking from label node
        dot.edge('team_label_node', 'maint_staff', style='invis')


    # Sales & Marketing Team
    with team_cluster.subgraph(name='cluster_sales_team') as sales_team:
        sales_team.attr(label='Sales & Marketing', **cluster_common_attrs)
        sales_team.node('front_desk', 'Front Desk Executives', fillcolor=colors['staff'])
        sales_team.node('shop_cafe', 'Pro Shop / \nCafé Staff', fillcolor=colors['staff'])
        # Invisible edge for ranking from label node
        dot.edge('team_label_node', 'front_desk', style='invis') # Connect to one staff node


    # Coaching Academy Team
    with team_cluster.subgraph(name='cluster_coach_team') as coach_team:
        coach_team.attr(label='Coaching', **cluster_common_attrs)
        coach_team.node('coaches', 'Coaches', fillcolor=colors['staff'])
         # Invisible edge for ranking from label node
        dot.edge('team_label_node', 'coaches', style='invis')


    # Finance & Admin Team Cluster (no staff nodes shown)
    with team_cluster.subgraph(name='cluster_fin_team') as fin_team:
         fin_team.attr(label='Finance & Admin', **cluster_common_attrs)
         # Add dummy node *inside* this specific cluster if needed for spacing
         # fin_team.node('fin_dummy_inner', '', style='invis', width='0', height='0', label='')


# Edges from Managers to Staff (visible reporting lines)
dot.edge('ops_mgr', 'maint_staff')
dot.edge('sales_mgr', 'front_desk')
dot.edge('sales_mgr', 'shop_cafe')
dot.edge('head_coach', 'coaches')


# --- Render and Save the Chart ---
try:
    dot.render(output_filename, format=output_format, view=view_chart_after_creation, cleanup=True)
    print(f"Org chart saved as '{output_filename}.{output_format}'")
    if view_chart_after_creation:
        print("Attempting to open the chart...")
except graphviz.exceptions.ExecutableNotFound:
    print("\n--- ERROR ---")
    print("Graphviz executable not found...") # Shortened error msg
except Exception as e:
    print(f"\n--- An error occurred during rendering: ---")
    print(e)
