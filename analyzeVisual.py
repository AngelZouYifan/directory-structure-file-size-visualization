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

### Process json data and output to csv files
# path = './Instagram_20221009/ads_and_businesses/advertisers_using_your_activity_or_information.json'
# save_to = './Instagram_sheets'

# path = 'Tasks.json'
# save_to = 'google_tasks.csv'

# with open(path) as json_file:
#     json_data = json.load(json_file)
# detailed_data = json_data["items"][0]["items"] # specify different route according to docs

# csv_file = open(save_to, 'w')
# csv_writer = csv.writer(csv_file)
# header = ['due','created','title','updated','status']
# csv_writer.writerow(header)
# for task in detailed_data:
#     try:
#         row = []
#         for attr in header:
#             row.append(task[attr])
#         csv_writer.writerow(row)
#     except:
#         continue
# csv_file.close()


### Analyze folder structures
# https://janakiev.com/blog/python-filesystem-analysis/#exploring-file-distributions-and-zipfs-law

# read from data download folder
# path_fldr = ''
# df = folderstats.folderstats(path_fldr, ignore_hidden=True)
# df = df.rename(columns={'name': 'text_name'})     # default 'name' causes weird error

# read from csv containing folder info (get from cml by `folderstats [FOLDER_PATH]/ -p -i -v -o [FILE_PATH].csv``)
path_sheet = './instagram_sheets/instagram.csv'
# path_sheet = './google_sheets/google.csv'
# path_sheet = './google_sheets/google_small.csv'
df = pd.read_csv(path_sheet)

df_sorted = df.sort_values(by='id')

# Initliaze graph with networkx
G = nx.Graph()
for i, row in df_sorted.iterrows(): 
    if row['parent'] != 0:
        G.add_edge(row['id'], row['parent'])
    else:
        G.add_node(row['id'])
    G.nodes[row['id']]['text_name'] = row['text_name'] 
    G.nodes[row['id']]['size'] = row['size']

### Graphviz Layout Dot 
# pos_dot = graphviz_layout(G, prog='dot')
# fig = plt.figure(figsize=(16, 9))
# nodes_attr_size = nx.get_node_attributes(G,'size')    # node size vary with folder/file size
# # nodes_size = [size/7000 for size in nodes_attr_size.values()] # instagram
# nodes_size = [size/10000+2 for size in nodes_attr_size.values()] # google
# nodes = nx.draw_networkx_nodes(G, pos_dot, node_size=nodes_size, node_color='C1')
# edges = nx.draw_networkx_edges(G, pos_dot, edge_color='C3', width=0.5)
# # this is commented because it only supports uniform font size
# # labels = nx.draw_networkx_labels(G, pos_dot, labels = nodes_attr_name, font_size = nodes_size)
# nodes_attr_name = nx.get_node_attributes(G,'text_name')
# for node, (x, y) in pos_dot.items():
#     # plt.text(x, y, nodes_attr_name[node], fontsize=nodes_attr_size[node]/1000000, ha='center', va='bottom') # instagram
#     plt.text(x, y, nodes_attr_name[node], fontsize=math.log(nodes_attr_size[node]/100+2), ha='left', va='bottom') # google
# # refer to this post for varying font size according to node size
# # https://stackoverflow.com/questions/62649745/is-it-possible-to-change-font-sizes-according-to-node-sizes
# # TBC: cannot truncate the names due to float type 
# plt.axis('off')
# # plt.show()    # for debugging
# # fig.savefig('instagram.svg', format='svg', dpi=1200)
# fig.savefig('google.svg', format='svg', dpi=1200)


### Graphviz Layout Twopi
pos_twopi = graphviz_layout(G, prog='twopi', root=1)    # 
fig = plt.figure(figsize=(16, 16))
nodes_attr_size = nx.get_node_attributes(G,'size')  # node size vary with folder/file size
# nodes_size = [size/10000 for size in nodes_attr_size.values()]   # for instagram
# nodes_size = [size/10000+2 for size in nodes_attr_size.values()]   # for google
nodes_size = [size/3000+2 for size in nodes_attr_size.values()]   # exaggeration
nodes = nx.draw_networkx_nodes(G, pos_twopi, node_size=nodes_size, alpha=0.6, node_color='C9') # node_color='C9'
edges = nx.draw_networkx_edges(G, pos_twopi, edge_color='C0', width=0.5)
nodes_attr_name = nx.get_node_attributes(G,'text_name')
for node, (x, y) in pos_twopi.items():
    plt.text(x, y, nodes_attr_name[node], fontsize=nodes_attr_size[node]/700000, 
             color='C4', ha='center', va='center') # for instagram
    # plt.text(x, y, nodes_attr_name[node], fontsize=math.log(nodes_attr_size[node]/100+2), ha='left', va='bottom') # for google
# refer to this post for varying font size according to node size
# https://stackoverflow.com/questions/62649745/is-it-possible-to-change-font-sizes-according-to-node-sizes
# TBC: cannot truncate the names due to float type 
plt.axis('off')
plt.axis('equal')
# plt.show()
fig.savefig('instagram_twopi_weirdsize.svg', format='svg', dpi=1200)
# fig.savefig('google_twopi_weirdFonts.svg', format='svg', dpi=1200)