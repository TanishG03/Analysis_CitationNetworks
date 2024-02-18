import networkx as nx
import matplotlib.pyplot as plt
import community
from datetime import datetime
from networkx.algorithms.community.centrality import girvan_newman

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

def detect_communities_girvan_newman(graph):
    # Use Girvan-Newman algorithm to detect communities
    communities_generator = girvan_newman(graph)
    # Choose the desired number of communities or stop criterion
    desired_communities = 2  # You can adjust this number
    communities = next(communities_generator)
    for i in range(desired_communities - 1):
        communities = next(communities_generator)
    return communities

def plot_girvan_newman_communities(graph, communities, pos, degree_threshold):
    node_colors = [0] * graph.number_of_nodes()
    
    for idx, comm in enumerate(communities):
        for node in comm:
            node_colors[node] = idx + 1

    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(set(node_colors)))
    nx.draw_networkx_nodes(graph, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(graph, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks()
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label(f'Community')
    
    plt.title(f'Communities (Girvan-Newman Algorithm) - Degree >= {degree_threshold}')
    plt.show()


def analyze_temporal_slices(citation_network, start_year, end_year, step=1):
    for year in range(start_year, end_year + 1, step):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + step, 1, 1)

        # Filter nodes with non-empty date information
        filtered_nodes = [node for node in citation_network.nodes if citation_network.nodes[node]['date'] and start_date <= datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]
        
        filtered_network = citation_network.subgraph(filtered_nodes)
        # degree_threshold = 10
        filtered_degrees = dict(filtered_network.degree())

        # Count the number of common edges within each year
        common_edges = 0
        for edge in filtered_network.edges:
            if edge[0] in filtered_nodes and edge[1] in filtered_nodes:
                common_edges += 1

        print(f"Time Frame: {year}-{year+step-1}, Number of Nodes: {filtered_network.number_of_nodes()}, Number of Edges: {filtered_network.number_of_edges()}, Number of Common Edges: {common_edges}")
    
        # plot2(filtered_degrees, filtered_network, degree_threshold, title=f'Citation Network - {year}-{year+step-1}')
    return filtered_network

def analyze_connected_citations(citation_network, start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1)  # Adding 1 to the end year to include citations up to the end year

    # Filter nodes with non-empty date information within the specified time frame
    filtered_nodes = [node for node in citation_network.nodes if citation_network.nodes[node]['date'] and start_date <= datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]
    filtered_network = citation_network.subgraph(filtered_nodes)

    # Create a dictionary mapping node identifiers to their respective year names
    year_labels = {node: datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d").strftime("%Y") for node in filtered_network.nodes}

    # Get unique years and assign a color to each year
    unique_years = list(set(year_labels.values()))
    color_map = plt.cm.get_cmap('tab10', len(unique_years))

    # Assign colors to nodes based on years
    node_colors = [color_map(unique_years.index(year)) for year in year_labels.values()]
    return filtered_network

def main():
    dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"
    date_file_path = "./Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)
        degree_threshold = 0
        filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
        filtered_network_degree = citation_network.subgraph(filtered_nodes)
        filtered_degrees = dict(filtered_network_degree.degree())
        
        # Analyze temporal slices
        temporal_filtered_network = analyze_temporal_slices(citation_network, 1998, 1998, step=1)
        
        # Analyze connected citations
        connected_filtered_network = analyze_connected_citations(filtered_network_degree, 1998, 1998)
        # Girvan-Newman community detection
        communities_girvan_newman = next(girvan_newman(connected_filtered_network))
        partition_girvan_newman = {node: idx for idx, comm in enumerate(communities_girvan_newman) for node in list(comm)}
        
        pos_girvan_newman = nx.spring_layout(connected_filtered_network, seed=13648)

        # Plot communities for Girvan-Newman
        plot_girvan_newman_communities(connected_filtered_network, communities_girvan_newman, pos_girvan_newman, degree_threshold)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()