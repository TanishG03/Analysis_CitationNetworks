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

def print_network_properties(citation_network, degree_threshold):
    filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
    filtered_network = citation_network.subgraph(filtered_nodes)

    print("Network Properties:")
    print("Number of Nodes:", filtered_network.number_of_nodes())
    print("Number of Edges:", filtered_network.number_of_edges())
    print("Average Degree:", np.mean(list(dict(filtered_network.degree()).values())))
    print("Density:", nx.density(filtered_network))

    # Diameter calculation may take time for large networks
    try:
        diameter = nx.diameter(filtered_network)
        print("Diameter:", diameter)
    except nx.NetworkXError:
        print("Diameter calculation skipped (graph is not connected)")

    # Centrality measures
    degree_centrality = nx.degree_centrality(filtered_network)
    betweenness_centrality = nx.betweenness_centrality(filtered_network)

    # Plot network with node color indicating degree centrality
    plot(filtered_network, degree_centrality, degree_threshold, "Degree Centrality")

    # Plot network with node color indicating betweenness centrality
    plot(filtered_network, betweenness_centrality, degree_threshold, "Betweenness Centrality")

    # Other properties
    # eccentricity = nx.eccentricity(filtered_network)
    closeness_centrality = nx.closeness_centrality(filtered_network)

    # Plot network with node color indicating eccentricity
    # plot(filtered_network, eccentricity, degree_threshold, "Eccentricity")

    # Plot network with node color indicating closeness centrality
    plot(filtered_network, closeness_centrality, degree_threshold, "Closeness Centrality")

def plot(filtered_network, centrality_values, degree_threshold, title):
    pos = nx.spring_layout(filtered_network, seed=42)
    node_colors = [centrality_values[node] for node in filtered_network.nodes]
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    plt.figure(figsize=(10, 8))
    nodes = nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap,
                                   edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])

    # Create an Axes object for the colorbar
    cax = plt.axes([0.85, 0.2, 0.02, 0.6])  # [left, bottom, width, height]

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1, cax=cax)  
    cbar.set_label(title)

    plt.title(f'Citation Network - Degree Threshold: {degree_threshold} - {title}')
    plt.show()

def main():
    # dataset_path = "./Datasets/cit-HepPh.txt/Cit-HepPh.txt"
    dataset_path = "./Datasets/cit-HepPh.txt/sample_10000.txt"
    # dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"

    try:
        citation_network = load_citation_network(dataset_path)
        degree_threshold = 10
        filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
        filtered_network = citation_network.subgraph(filtered_nodes)
        filtered_degrees = dict(filtered_network.degree())
        # plot(filtered_degrees, filtered_network,degree_threshold)
        print_network_properties(citation_network, degree_threshold)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
