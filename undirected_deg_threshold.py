import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def load_citation_network(file_path):
    # graph = nx.DiGraph()  
    graph = nx.Graph()  

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            source, target = map(int, line.strip().split())
            graph.add_node(source)
            graph.add_node(target)
            graph.add_edge(source, target)

    return graph

def plot(filtered_network, degree_threshold):
    filtered_degrees = dict(filtered_network.degree())
    node_colors = list(filtered_degrees.values())
    
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label('Node Degree')
    print(len(filtered_network.nodes))
    print(len(filtered_network.edges))
    print(list(filtered_degrees.values()))
    plt.show()

def main():
    # dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"
    # dataset_path = "./Datasets/cit-HepPh.txt/sample_100.txt"
    dataset_path = "./Datasets/cit-HepPh.txt/sample_200.txt"

    try:
        citation_network = load_citation_network(dataset_path)
        degree_threshold = 0
        # original_degrees = dict(citation_network.degree())
        # print("Original degrees:", original_degrees)
        # print(len(original_degrees))
        # Ensure that only nodes with degrees greater than or equal to the threshold are included
        # filtered_nodes = [node for node in citation_network.nodes if citation_network.out_degree(node) >= degree_threshold]
        filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
        filtered_network = citation_network.subgraph(filtered_nodes)    
        # filtered_degrees = dict(filtered_network.degree())
        # print("Filtered degrees:", filtered_degrees)
        # print(len(filtered_degrees))
        plot(filtered_network, degree_threshold)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()

# 1-deg_0_without_date_undirected