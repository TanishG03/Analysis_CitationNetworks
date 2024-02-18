import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def load_citation_network(file_path):
    graph = nx.DiGraph()  

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            source, target = map(int, line.strip().split())
            graph.add_node(source)
            graph.add_node(target)
            graph.add_edge(source, target)

    return graph

def plot(filtered_degrees, filtered_network, degree_threshold):
    # degree_threshold = 10
    node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nodes = nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap,
                                   edgecolors='k', linewidths=0.5)
    edges = nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable

    # Specify the Axes for the Colorbar
    cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label(f'Node Degree >= {degree_threshold}')
    plt.show()

    
def main():
    # dataset_path = "./Datasets/cit-HepPh.txt/Cit-HepPh.txt"
    # dataset_path = "./Datasets/cit-HepPh.txt/sample_100.txt"
    dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"

    try:
        citation_network = load_citation_network(dataset_path)
        degree_threshold = 2
        filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
        filtered_network = citation_network.subgraph(filtered_nodes)
        filtered_degrees = dict(filtered_network.degree())
        plot(filtered_degrees, filtered_network,degree_threshold)

    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()