import networkx as nx
import matplotlib.pyplot as plt
import community
from datetime import datetime

def load_citation_network(file_path, date_file_path):
    graph = nx.Graph()

    # Load date information
    node_dates = {}
    with open(date_file_path, 'r') as date_file:
        for line in date_file:
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            node = int(parts[0])
            date_str = parts[1]
            node_dates[node] = date_str

    # Load citation network with date filtering
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            source, target = map(int, line.strip().split())

            # Check if both source and target nodes have valid dates
            if source in node_dates and target in node_dates:
                source_date = node_dates[source]
                target_date = node_dates[target]

                # Add nodes with date information as attributes
                graph.add_node(source, date=source_date)
                graph.add_node(target, date=target_date)
                graph.add_edge(source, target)

    return graph

def plot_communities(graph, partition, pos, degree_threshold, title=''):
    node_colors = [partition[node] for node in graph.nodes]

    if not node_colors:
        print("No nodes to plot.")
        return

    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(set(node_colors)))
    nx.draw_networkx_nodes(graph, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label(f'Community')

    plt.title(title)
    plt.show()

def temporal_community_detection(citation_network, start_year, end_year, step=1):
    for year in range(start_year, end_year + 1, step):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + step, 1, 1)

        # Filter nodes with non-empty date information
        filtered_nodes = [node for node in citation_network.nodes if
                          citation_network.nodes[node]['date'] and start_date <= datetime.strptime(
                              citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]

        filtered_network = citation_network.subgraph(filtered_nodes)
        degree_threshold = 10
        filtered_degrees = dict(filtered_network.degree())

        # Louvain community detection
        partition = community.best_partition(filtered_network)
        pos = nx.spring_layout(filtered_network, seed=13648)

        # Plot communities for each temporal slice
        plot_communities(filtered_network, partition, pos, degree_threshold,
                         title=f'Communities (Louvain Algorithm) - {year}-{year + step - 1}')

def main():
    dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"
    date_file_path = "./Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)

        # Analyze temporal slices and perform community detection
        temporal_community_detection(citation_network, 2005, 2005, step=1)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
