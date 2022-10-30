import csv
import os
import json
import networkx as nx
import pandas as pd
import numpy as np
import folderstats
import matplotlib as mpl
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import math

### Analyze folder structures
# https://janakiev.com/blog/python-filesystem-analysis/#exploring-file-distributions-and-zipfs-law

# read from data download folder
path_fldr = ''
df = folderstats.folderstats(path_fldr, ignore_hidden=True)
df = df.rename(columns={'name': 'text_name'})     # default 'name' causes weird error

# read from csv containing folder info (get from command line by `folderstats [FOLDER_PATH]/ -p -i -v -o [FILE_PATH].csv``)
# path_sheet = ''
# df = pd.read_csv(path_sheet)

df_sorted = df.sort_values(by='id')

### Initliaze graph with networkx
G = nx.Graph()
for i, row in df_sorted.iterrows(): 
    if row['parent'] != 0:
        G.add_edge(row['id'], row['parent'])
    else:
        G.add_node(row['id'])
    G.nodes[row['id']]['text_name'] = row['text_name'] 
    G.nodes[row['id']]['size'] = row['size']

### Graphviz Layout Twopi
pos_twopi = graphviz_layout(G, prog='twopi', root=1)    
fig = plt.figure(figsize=(16, 16))
nodes_attr_size = nx.get_node_attributes(G,'size')  # node size vary with folder/file size
nodes_size = [math.log(size/1000+2) for size in nodes_attr_size.values()]   # sample normalization
nodes = nx.draw_networkx_nodes(G, pos_twopi, node_size=nodes_size, alpha=0.6, node_color='C9') 
edges = nx.draw_networkx_edges(G, pos_twopi, edge_color='C0', width=0.5)
nodes_attr_name = nx.get_node_attributes(G,'text_name')
for node, (x, y) in pos_twopi.items():
    plt.text(x, y, nodes_attr_name[node], fontsize=math.log(nodes_attr_size[node]/1000+2), # normalization
             color='C4', ha='center', va='center')
plt.axis('off')
plt.axis('equal')
plt.show()  # show graph in separate window
# fig.savefig('', format='svg', dpi=1200)   # save to svg file