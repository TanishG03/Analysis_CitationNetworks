import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from community import community_louvain

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

def plot_communities(graph, partition, pos, degree_threshold, title='', ax=None):
    node_colors = [partition[node] for node in graph.nodes]

    if not node_colors:
        print("No nodes to plot.")
        return

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))

    cmap = plt.cm.get_cmap("rainbow", len(set(node_colors)))
    nx.draw_networkx_nodes(graph, pos, node_size=50, node_color=node_colors, cmap=cmap, ax=ax, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(graph, pos, alpha=0.1, ax=ax)
    ax.set_xticks([])
    ax.set_yticks([])

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1, ax=ax)
    cbar.set_label(f'Community')

    ax.set_title(title)
    plt.show()

def calculate_community_statistics(partition):
    community_sizes = [len([node for node, part in partition.items() if part == community]) for community in set(partition.values())]
    total_nodes = len(partition)

    largest_community_size = max(community_sizes)
    largest_community_percentage = (largest_community_size / total_nodes) * 100

    independent_nodes = total_nodes - sum(community_sizes)
    independent_percentage = (independent_nodes / total_nodes) * 100

    print(f"Total nodes: {total_nodes}")
    print(f"Largest community size: {largest_community_size} ({largest_community_percentage:.2f}%)")
    print(f"Independent nodes: {independent_nodes} ({independent_percentage:.2f}%)")

    return community_sizes

def calculate_top_community_percentage(community_sizes, top_n=3):
    top_community_sizes = sorted(community_sizes, reverse=True)[:top_n]
    total_nodes_in_top_communities = sum(top_community_sizes)
    total_nodes = sum(community_sizes)
    
    top_community_percentage = (total_nodes_in_top_communities / total_nodes) * 100

    print(f"\nTop {top_n} Community Sizes: {top_community_sizes}")
    print(f"Percentage of Nodes in Top {top_n} Communities: {top_community_percentage:.2f}%")

def temporal_community_cumulation(citation_network, start_year, end_year, step=1):
    all_partitions = {}  # Dictionary to store partitions for each year

    for year in range(start_year, end_year + 1, step):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + step, 1, 1)
        
        # Filter nodes with non-empty date information
        filtered_nodes = [node for node in citation_network.nodes if
                          citation_network.nodes[node]['date'] and start_date <= datetime.strptime(
                              citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]
        
        # Create a subgraph for the current time frame
        filtered_network = citation_network.subgraph(filtered_nodes)

        # Louvain community detection
        partition = community_louvain.best_partition(filtered_network, resolution=1.0, randomize=False)
        
        # Store the partition for the current year
        all_partitions[year] = partition

        pos = nx.spring_layout(filtered_network, seed=13648)

        # Plot communities for each temporal slice
        plot_communities(filtered_network, partition, pos, 0,
                         title=f'Communities (Louvain Algorithm) - {year}-{year + step - 1}')

        # Calculate and print community statistics
        print(f"\nCommunity Statistics for {year}-{year + step - 1}:")
        community_sizes = calculate_community_statistics(partition)

        # Calculate and print top community percentage
        calculate_top_community_percentage(community_sizes, top_n=3)

if __name__ == "__main__":
    dataset_path = "./Datasets/cit-HepPh.txt/sample_10000.txt"
    date_file_path = "./Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)

        # Analyze temporal slices and perform community detection with cumulation
        temporal_community_cumulation(citation_network, 1994, 2001, step=3)

    except Exception as e:
        print("Error:", str(e))
