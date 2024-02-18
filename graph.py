import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

def update_plot(frame, ax, filtered_network, degree_threshold, sc, cbar):
    ax.clear()
    
    # Add one node at a time
    node_to_add = list(filtered_network.nodes())[frame]
    filtered_network.add_node(node_to_add)
    
    filtered_nodes = [node for node in filtered_network.nodes if filtered_network.degree(node) >= degree_threshold]
    subgraph = filtered_network.subgraph(filtered_nodes)
    filtered_degrees = dict(subgraph.degree())

    node_colors = [filtered_degrees[node] for node in subgraph.nodes]
    pos = nx.spring_layout(subgraph, seed=13648)

    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    sc = nx.draw_networkx_nodes(subgraph, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5, ax=ax)
    nx.draw_networkx_edges(subgraph, pos, alpha=0.1, ax=ax)

    ax.set_xticks([])
    ax.set_yticks([])

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar.mappable.set_array([])  # Clear the color bar data
    cbar.mappable.set_array(node_colors)  # Set the color bar data to the new values
    cbar.mappable.set_clim(vmin=degree_threshold, vmax=max(node_colors))

    return sc  # Return the scatter plot to update in the animation

def main():
    dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"
    
    try:
        citation_network = load_citation_network(dataset_path)
        degree_threshold = 0
        filtered_network = citation_network.copy()  # Initial graph is the entire network

        fig, ax = plt.subplots(figsize=(8, 6))
        sm = plt.cm.ScalarMappable(cmap='rainbow')  # Initialize sm
        cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1, ax=ax)
        ani = FuncAnimation(fig, update_plot, frames=len(filtered_network.nodes),
                            fargs=(ax, filtered_network, degree_threshold, None, cbar), interval=200, repeat=False)

        plt.show()

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
