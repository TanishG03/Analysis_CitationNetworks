import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

def load_citation_network(file_path, date_file_path):
    graph = nx.DiGraph()

    # Load date information from the file
    date_dict = {}
    with open(date_file_path, 'r') as date_file:
        for line in date_file:
            if line.startswith("#"):
                continue
            paper_id, date_str = line.strip().split()
            date_dict[int(paper_id)] = date_str

    # Load citation network from the main file
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            source, target = map(int, line.strip().split())
            graph.add_node(source, date=date_dict.get(source, ""))
            graph.add_node(target, date=date_dict.get(target, ""))
            graph.add_edge(source, target)

    return graph

def plot(filtered_degrees, filtered_network, degree_threshold, title="Citation Network"):
    node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nodes = nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    
    # Add labels with dates
    date_labels = {node: filtered_network.nodes[node]['date'] for node in filtered_network.nodes}
    nx.draw_networkx_labels(filtered_network, pos, labels=date_labels, font_size=8, font_color='black')

    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1, ax=ax)  
    cbar.set_label(f'Node Degree >= {degree_threshold}')
    plt.title(title)
    plt.show()

def plot2(filtered_degrees, filtered_network, degree_threshold, title="Citation Network"):
    node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nodes = nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    
    # Add labels with dates
    date_labels = {node: filtered_network.nodes[node]['date'] for node in filtered_network.nodes}
    nx.draw_networkx_labels(filtered_network, pos, labels=date_labels, font_size=8, font_color='black')

    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1, ax=ax)  
    cbar.set_label(f'Node Degree >= {degree_threshold}')
    plt.title(title)
    plt.annotate(f'Number of Nodes: {filtered_network.number_of_nodes()} and Number of Edges: {filtered_network.number_of_edges()}', xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=10)

    plt.show()

def analyze_temporal_slices(citation_network, start_year, end_year, step=1):
    for year in range(start_year, end_year + 1, step):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + step, 1, 1)

        # Filter nodes with non-empty date information
        filtered_nodes = [node for node in citation_network.nodes if citation_network.nodes[node]['date'] and start_date <= datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]
        
        filtered_network = citation_network.subgraph(filtered_nodes)
        degree_threshold = 10
        filtered_degrees = dict(filtered_network.degree())

        # Count the number of common edges within each year
        common_edges = 0
        for edge in filtered_network.edges:
            if edge[0] in filtered_nodes and edge[1] in filtered_nodes:
                common_edges += 1

        print(f"Time Frame: {year}-{year+step-1}, Number of Nodes: {filtered_network.number_of_nodes()}, Number of Edges: {filtered_network.number_of_edges()}, Number of Common Edges: {common_edges}")

        plot2(filtered_degrees, filtered_network, degree_threshold, title=f'Citation Network - {year}-{year+step-1}')

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

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

    # Use Fruchterman-Reingold layout for a force-directed graph layout
    pos = nx.spring_layout(filtered_network, seed=42)
    print(f"Time Frame: {start_year}-{end_year}, Number of Nodes: {filtered_network.number_of_nodes()}, Number of Edges: {filtered_network.number_of_edges()}")


    # Plot the subgraph with year names as labels
    nx.draw(filtered_network, pos, with_labels=True, labels=year_labels, node_size=50, node_color=node_colors, edge_color='gray', alpha=0.7)

    # Add legend
    legend_labels = {unique_years[i]: color_map(i) for i in range(len(unique_years))}
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_labels.values()]
    plt.legend(legend_handles, legend_labels.keys(), title='Years')

    # Add time frame, number of nodes, and number of edges as annotations
    plt.annotate(f'Time Frame: {start_year}-{end_year}', xy=(0.5, 1.02), xycoords='axes fraction', ha='center', fontsize=10)
    plt.annotate(f'Number of Nodes: {filtered_network.number_of_nodes()} and Number of Edges: {filtered_network.number_of_edges()}', xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=10)
    # plt.annotate(f'Number of Edges: {filtered_network.number_of_edges()}', xy=(0.5, 0.90), xycoords='axes fraction', ha='center', fontsize=10)

    plt.title(f'Citation Network - {start_year}-{end_year}')
    plt.show()

# Example usage
# analyze_connected_citations(your_citation_network, 2000, 2020)



# Rest of the code...


# Rest of the code...
def main():
    dataset_path = "./Datasets/cit-HepPh.txt/sample_10000.txt"
    date_file_path = "Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)
        degree_threshold = 10
        filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
        filtered_network = citation_network.subgraph(filtered_nodes)
        filtered_degrees = dict(filtered_network.degree())
        plot(filtered_degrees, filtered_network, degree_threshold)
        
        # Temporal Slicing Analysis
        # analyze_temporal_slices(citation_network, 1998, 2000, step=1)
        analyze_connected_citations(citation_network, 1991, 1992)
        analyze_connected_citations(citation_network, 1990, 1991)
        analyze_connected_citations(citation_network, 1996, 1997)
        analyze_connected_citations(citation_network, 1997, 1998)
        analyze_connected_citations(citation_network, 1998, 1999)
        analyze_connected_citations(citation_network, 1999, 2000)


        
        # Dynamic Analysis
        # dynamic_analysis(citation_network, 2000, 2010, step=1)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()





