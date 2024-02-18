import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

def load_citation_network(file_path, date_file_path):
    graph = nx.DiGraph()  

    # Load dates from the separate dataset file
    node_dates = {}
    with open(date_file_path, 'r') as date_file:
        for line in date_file:
            data = line.strip().split()
            if len(data) == 2:
                node, date_str = data
                date = datetime.strptime(date_str, "%Y-%m-%d")  # Adjust the format as per your data
                node_dates[node] = date

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            source, target = map(str.strip, line.split())

            # Add nodes with their respective dates
            if source not in graph.nodes:
                graph.add_node(source, date=node_dates.get(source, None))
            if target not in graph.nodes:
                graph.add_node(target, date=node_dates.get(target, None))

            # Add edge with the date
            graph.add_edge(source, target)

    return graph

# Add a function to filter the network based on the date
def filter_network_by_date(network, start_date, end_date):
    filtered_nodes = [
        node for node, attr in network.nodes(data=True) 
        if attr.get('date', datetime.min) is not None and start_date <= attr['date'] <= end_date
    ]
    filtered_network = network.subgraph(filtered_nodes)
    return filtered_network


def plot(filtered_network, degree_threshold):
    filtered_degrees = dict(filtered_network.degree())
    
    if not filtered_degrees:
        print("No nodes with degrees above the threshold.")
        return

    node_colors = list(filtered_degrees.values())
    
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    # pos = nx.kamada_kawai_layout(filtered_network)

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
    dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"
    date_file_path = "./Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)
        degree_threshold = 10
        start_date = datetime(1998, 1, 1)  # Example start date
        end_date = datetime(2000, 12, 31)   # Example end date

        filtered_network = filter_network_by_date(citation_network, start_date, end_date)
        plot(filtered_network, degree_threshold)

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
