import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random
import arabic_reshaper
from bidi.algorithm import get_display
from Narrator import Narrator 

# File paths
file_path1 = 'annexe2_2hadith2.xlsx'
file_path2 = 'anexe2_1_hadith1.xlsx'

# Load data from Excel files
df_narrators = pd.read_excel(file_path1)
df_chains = pd.read_excel(file_path2, header=None, usecols=[0])

# Function to load narrators
def load_narrators(df):
    narrators = {}
    df.columns = ['fullName', 'name', 'birthDate', 'deathDate']
    for _, row in df.iterrows():
        narrators[row['fullName']] = Narrator(row['name'], row['birthDate'], row['deathDate'])
    return narrators

# Function to prepare chains
def prepare_chains(df):
    chains = {}
    current_chain = []
    current_key = 1
    for _, row in df.iterrows():
        text = row[0]
        if isinstance(text, str):
            if "سلسلة رواة الحديث عدد" in text:
                if current_chain:
                    chains[current_key] = current_chain
                    current_chain = []
                    current_key += 1
            else:
                current_chain.append(text.strip())
    if current_chain:
        chains[current_key] = current_chain

    # Clean narrator names
    for key, value in chains.items():
        chains[key] = [narrator.replace('\xa0', ' ').strip() for narrator in value]

    return chains

# Function to define positions with increased spacing
def define_positions(narrators, chains):
    pos = {}
    x_spacing = 10  
    y_spacing = -2  
    chain_offset = 0 

    for chain_key, chain in chains.items():
        for idx, narrator in enumerate(chain):
            y_pos = idx * y_spacing
            x_pos = chain_offset
           
            if narrator in narrators and pd.notna(narrators[narrator].birthDate):
                x_pos += narrators[narrator].birthDate / 100.0 
            pos[narrator] = (x_pos, y_pos)
        chain_offset += x_spacing 
    return pos

# Load narrators and chains
narrators = load_narrators(df_narrators)
chains = prepare_chains(df_chains) 

# Reshape Arabic text for correct display
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text) 
    bidi_text = get_display(reshaped_text)  
    return bidi_text

# Apply reshaping to chains
for chain_key in chains:
    chains[chain_key] = [reshape_text(narrator) for narrator in chains[chain_key]]

# Build the graph
G = nx.DiGraph()
for chain in chains.values():
    for i in range(len(chain) - 1):
        G.add_node(chain[i])
        G.add_edge(chain[i], chain[i + 1])
    G.add_node(chain[-1])  

# Abbreviate names
def abbreviate_name(name):
    parts = name.split()  
    if len(parts) > 2:  
        return f"{parts[0]} {parts[1][0]}."  
    return name  

# Apply abbreviation to the nodes
abbreviated_names = {narrator: abbreviate_name(narrator) for narrator in G.nodes}

# Define positions
positions = define_positions(narrators, chains)

# Visualization
plt.figure(figsize=(20, 15))

# Assign node colors
node_colors = {node: '#c3e0e5' for node in G.nodes}  
for chain in chains.values():
    if chain:
        node_colors[chain[0]] = '#41729f' 

# Convert to a list of colors
color_list = [node_colors[node] for node in G.nodes]

# Draw nodes
nx.draw_networkx_nodes(G, positions, node_size=3000, node_color=color_list)

# Draw labels
nx.draw_networkx_labels(G, positions, font_size=7, font_weight="bold")

# Draw edges with curved paths around nodes
for chain in chains.values():
    edge_color = f"#{''.join(random.choice('0123456789ABCDEF') for _ in range(6))}"
    edges = [(chain[i], chain[i + 1]) for i in range(len(chain) - 1)]
    for u, v in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 1  
        arc_pos = [(x1, y1), (mid_x, mid_y), (x2, y2)]
        nx.draw_networkx_edges(
            G,
            positions,
            edgelist=[(u, v)],
            edge_color=edge_color,
            connectionstyle="arc3,rad=0.15",  
            arrows=True,
            arrowsize=15
        )

# Finalize plot
plt.title("Hadith Transmission Chains with Routed Edges")
plt.gca().invert_xaxis()
plt.axis("off")
plt.show()
