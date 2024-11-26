import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import random

# Load narrators and chains data
df_narrators = pd.read_excel('annexe2_2hadith2.xlsx')
df_chains = pd.read_excel('anexe2_1_hadith1.xlsx', header=None, usecols=[0])

# Load narrators into a dictionary
class Narrator:
    def __init__(self, name, birth_date, death_date):
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date

def load_narrators(df):
    narrators = {}
    df.columns = ['fullName', 'name', 'birthDate', 'deathDate']
    for _, row in df.iterrows():
        name = row['name'] if pd.notna(row['name']) else row['fullName']
        narrators[row['fullName']] = Narrator(name, row['birthDate'], row['deathDate'])
    return narrators

narrators = load_narrators(df_narrators)

# Prepare hadith chains
def prepare_chains(df):
    chains = {}
    current_chain = []
    current_key = 1
    for _, row in df.iterrows():
        text = row[0]
        if isinstance(text, str) and "سلسلة رواة الحديث عدد" in text:
            if current_chain:
                chains[current_key] = current_chain
                current_chain = []
                current_key += 1
        else:
            current_chain.append(text.strip())
    if current_chain:
        chains[current_key] = current_chain
    return chains

chains = prepare_chains(df_chains)

# Reshape Arabic text for correct display
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  
    bidi_text = get_display(reshaped_text) 
    return bidi_text

# Apply reshaping to chains
for chain_key in chains:
    chains[chain_key] = [reshape_text(narrator) for narrator in chains[chain_key]]

# Create a directed graph for each chain and combine them
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

# Custom layout function with vertical alignment for narrators at the same index
def vertical_alignment_layout(G, chains_data):
    pos = {}
    x_offset = 0  
    y_spacing = -1 

    for chain in chains_data.values():
        for idx, node in enumerate(chain):
            pos[node] = (x_offset, y_spacing * idx)  
        x_offset += 5 

    return pos

# Generate positions
pos = vertical_alignment_layout(G, chains)

plt.figure(figsize=(20, 15))

# Draw nodes with specified colors
node_colors = {node: '#c3e0e5' for node in G.nodes}  
first_node_colors = {chain[0]: '#41729f' for chain in chains.values() if chain}  

# Update colors for first nodes
for node in first_node_colors:
    node_colors[node] = first_node_colors[node]

# Convert to a list of colors for drawing
color_list = [node_colors[node] for node in G.nodes]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=color_list)

# Draw labels
nx.draw_networkx_labels(G, 
                        pos,
                        font_size=7,
                        font_weight="bold"
                        )

# Draw edges with different colors for each chain
for chain_key, chain in chains.items():
    color = f"#{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])}"  
    edges = [(chain[i], chain[i - 1]) for i in range(1, len(chain))]
    nx.draw_networkx_edges(
        G, 
        pos,
        edgelist=edges,
        edge_color=color,
        connectionstyle="arc3,rad=0.1",
        arrows=True,
        arrowsize=15
    )

plt.title("Hadith Transmission Chains")
plt.gca().invert_xaxis()  
plt.axis("off")  
plt.show()
