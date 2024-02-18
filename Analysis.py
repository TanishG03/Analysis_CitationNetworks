import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime 

def load_citation_network(file_path, date_file_path):
    graph = nx.DiGraph()
    # graph = nx.Graph()

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
def calculate_average_degree(citation_network, year_range):
    start_year, end_year = year_range

    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1)

    # Filter nodes with non-empty date information within the specified time frame
    filtered_nodes = [node for node in citation_network.nodes if 
                        citation_network.nodes[node]['date'] and 
                        start_date <= datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]

    filtered_network = citation_network.subgraph(filtered_nodes)

    # Calculate and print the average degree for the current year range
    average_degree = np.mean(list(dict(filtered_network.degree()).values()))
    print(f"Average Degree for {start_year}-{end_year}: {average_degree}")

def plot(filtered_degrees,filtered_network,degree_threshold):
    # degree_threshold =10
    node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label(f'Node Degree >= {degree_threshold}')
    plt.show()

def plot(filtered_degrees,filtered_network,degree_threshold,title):
    # degree_threshold =10
    node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
    seed = 13648
    pos = nx.spring_layout(filtered_network, seed)
    plt.figure(figsize=(10, 8))
    cmap = plt.cm.get_cmap("rainbow", len(node_colors))
    nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
    nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
    plt.xticks([])
    plt.yticks([])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
    sm._A = []  # Fix for ScalarMappable
    cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
    cbar.set_label(f'Node Degree >= {degree_threshold}')
    plt.table(title)
    plt.show()

def analyze_connected_citations(citation_network, start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year + 1, 1, 1)  

    filtered_nodes = [node for node in citation_network.nodes if citation_network.nodes[node]['date'] and start_date <= datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d") < end_date]

    filtered_network = citation_network.subgraph(filtered_nodes)
    year_labels = {node: datetime.strptime(citation_network.nodes[node]['date'], "%Y-%m-%d").strftime("%Y") for node in filtered_network.nodes}
    unique_years = list(set(year_labels.values()))
    color_map = plt.cm.get_cmap('tab10', len(unique_years))
    node_colors = [color_map(unique_years.index(year)) for year in year_labels.values()]

    pos = nx.spring_layout(filtered_network, seed=42)
    
    plt.figure(figsize=(10, 8))
    nx.draw(filtered_network, pos, with_labels=False, node_size=50, node_color=node_colors, edge_color='gray', alpha=0.7)
    
    legend_labels = {unique_years[i]: color_map(i) for i in range(len(unique_years))}
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_labels.values()]
    
    plt.legend(legend_handles, legend_labels.keys(), title='Years')
    plt.annotate(f'Time Frame: {start_year}-{end_year}', xy=(0.5, 1.02), xycoords='axes fraction', ha='center', fontsize=10)
    plt.annotate(f'Number of Nodes: {filtered_network.number_of_nodes()} and Number of Edges: {filtered_network.number_of_edges()}', xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=10)
    plt.title(f'Citation Network - {start_year}-{end_year}')
    plt.show()

    return filtered_network

def print_network_properties(citation_network, degree_threshold):
    filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
    filtered_network = citation_network.subgraph(filtered_nodes)

    print("Network Properties:")
    print("Number of Nodes:", filtered_network.number_of_nodes())
    print("Number of Edges:", filtered_network.number_of_edges())
    print("Average Degree:", np.mean(list(dict(filtered_network.degree()).values())))
    print("Density:", nx.density(filtered_network))

    # Diameter calculation may take time for large networks
    # try:
    #     diameter = nx.diameter(filtered_network)
    #     print("Diameter:", diameter)
    # except nx.NetworkXError:
    #     print("Diameter calculation skipped (graph is not connected)")

    # Centrality measures
    # degree_centrality = nx.degree_centrality(filtered_network)
    # betweenness_centrality = nx.betweenness_centrality(filtered_network)

    # Plot network with node color indicating degree centrality
    # plot(filtered_network, degree_centrality, degree_threshold, "Degree Centrality")

    # # Plot network with node color indicating betweenness centrality
    # plot(filtered_network, betweenness_centrality, degree_threshold, "Betweenness Centrality")

    # # Other properties
    # # eccentricity = nx.eccentricity(filtered_network)
    # closeness_centrality = nx.closeness_centrality(filtered_network)

    # # Plot network with node color indicating eccentricity
    # # plot(filtered_network, eccentricity, degree_threshold, "Eccentricity")

    # # Plot network with node color indicating closeness centrality
    # plot(filtered_network, closeness_centrality, degree_threshold, "Closeness Centrality")

def main():
    # dataset_path = "./Datasets/cit-HepPh.txt/Cit-HepPh.txt"
    # dataset_path = "./Datasets/cit-HepPh.txt/sample_200.txt"
    dataset_path = "./Datasets/cit-HepPh.txt/sample_10000.txt"
    date_file_path = "Datasets/cit-HepPh-dates.txt"


    try:
        citation_network = load_citation_network(dataset_path, date_file_path)
        
        degree_threshold = 0

        # Iterate through consecutive year ranges
        for start_year in range(1993, 2000):
            end_year = start_year + 1

            # Filter nodes based on degree and the current year range
            filtered_nodes = [node for node in citation_network.nodes if 
                            citation_network.degree(node) >= degree_threshold]
            
            filtered_network = citation_network.subgraph(filtered_nodes)
            filtered_degrees = dict(filtered_network.degree())
            filtered_network = analyze_connected_citations(filtered_network, start_year, end_year)
            
            print(f"\nNetwork properties for the year range {start_year}-{end_year}")
            calculate_average_degree(citation_network, (start_year, end_year))
            # connectedness(filtered_network)
            # degree_dis(filtered_network)
            # clustering(filtered_network)
            # community(filtered_network)
            # # vizualisation(filtered_network)
            # print_network_properties(citation_network, degree_threshold)

            # diameter(filtered_network)

    except Exception as e:
        print("Error:", str(e))




import matplotlib.pyplot as plt

def degree_dis(citation_network):
    degrees = [citation_network.degree(node) for node in citation_network.nodes]
    bins = range(1, 32)  # Define bins from 1 to 31 to include degrees 1 to 30
    plt.hist(degrees, bins=bins, alpha=0.7, align='left', rwidth=0.8)  # Set align and rwidth parameters
    plt.title('Degree Distribution')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.xticks(range(0, 31))  # Set x-axis ticks for each degree from 1 to 30
    plt.show()

# Example usage:
# Assuming citation_network is your network object (you need to have it defined before calling this function)
# degree_dis(citation_network)


def diameter(citation_network):
    if nx.is_strongly_connected(citation_network):
        diameter_value = nx.diameter(citation_network)
        print(f'Graph Diameter: {diameter_value}')
    else:
        print("The graph is not strongly connected.")
        # Calculate diameter for each strongly connected component
        for component in nx.strongly_connected_components(citation_network):
            component_subgraph = citation_network.subgraph(component)
            diameter_value = nx.diameter(component_subgraph)
            print(f'Diameter for a strongly connected component: {diameter_value}')


def centrality(citation_network):
    degree_centrality = nx.degree_centrality(citation_network)
    betweenness_centrality = nx.betweenness_centrality(citation_network)
    closeness_centrality = nx.closeness_centrality(citation_network)

def clustering(citation_network):
    clustering_coefficient = nx.average_clustering(citation_network)
    print(f'Average Clustering Coefficient: {clustering_coefficient}')

def connectedness(citation_network):
    num_strongly_connected_components = nx.number_strongly_connected_components(citation_network)
    print(f'Number of Strongly Connected Components: {num_strongly_connected_components}')


def community(citation_network):
    communities = nx.community.greedy_modularity_communities(citation_network)
    print(f'Number of Communities: {len(communities)}')

# def vizualisation(citation_network):
#     seed = 13648
#     pos = nx.spring_layout(citation_network, seed)

#     node_dates = nx.get_node_attributes(citation_network, 'date')

#     date_labels = {node: f"{node}\n{node_dates[node]}" for node in node_dates}

#     nx.draw(citation_network, pos, with_labels=False, node_size=50, alpha=0.7)
#     nx.draw_networkx_labels(citation_network, pos, labels=date_labels, font_size=8, font_color='r')
#     plt.show()
def vizualisation(citation_network):
    seed = 13648
    pos = nx.spring_layout(citation_network, seed)

    node_dates = nx.get_node_attributes(citation_network, 'date')
    years = [datetime.strptime(date, "%Y-%m-%d").strftime("%Y") for date in node_dates.values()]

    unique_years = list(set(years))
    color_map = plt.cm.get_cmap('tab10', len(unique_years))
    node_colors = [color_map(unique_years.index(year)) for year in years]

    plt.figure(figsize=(10, 8))
    nx.draw(citation_network, pos, with_labels=False, node_size=50, alpha=0.7, node_color=node_colors, cmap=color_map)
    
    legend_labels = {unique_years[i]: color_map(i) for i in range(len(unique_years))}
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map(i), markersize=10) for i in range(len(unique_years))]
    
    plt.legend(legend_handles, legend_labels.keys(), title='Years')
    plt.title('Citation Network with Node Colors representing Years')
    plt.show()



if __name__ == "__main__":
    main()


# import networkx as nx
# import matplotlib.pyplot as plt
# import numpy as np
# from datetime import datetime 

# def load_citation_network(file_path):
#     graph = nx.DiGraph()  

#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.startswith("#"):
#                 continue
#             source, target = map(int, line.strip().split())
#             graph.add_node(source)
#             graph.add_node(target)
#             graph.add_edge(source, target)

#     return graph

# def plot(filtered_degrees,filtered_network,degree_threshold):
#     # degree_threshold =10
#     node_colors = [filtered_degrees[node] for node in filtered_network.nodes]
#     seed = 13648
#     pos = nx.spring_layout(filtered_network, seed)
#     plt.figure(figsize=(10, 8))
#     cmap = plt.cm.get_cmap("rainbow", len(node_colors))
#     nx.draw_networkx_nodes(filtered_network, pos, node_size=50, node_color=node_colors, cmap=cmap, edgecolors='k', linewidths=0.5)
#     nx.draw_networkx_edges(filtered_network, pos, alpha=0.1)
#     plt.xticks([])
#     plt.yticks([])
#     sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=degree_threshold, vmax=max(node_colors)))
#     sm._A = []  # Fix for ScalarMappable
#     cbar = plt.colorbar(sm, orientation='vertical', fraction=0.02, pad=0.1)
#     cbar.set_label(f'Node Degree >= {degree_threshold}')
#     plt.show()
    
# def main():
#     # dataset_path = "./Datasets/cit-HepPh.txt/Cit-HepPh.txt"
#     # dataset_path = "./Datasets/cit-HepPh.txt/sample_100.txt"
#     dataset_path = "./Datasets/cit-HepPh.txt/sample_5000.txt"

#     try:
#         citation_network = load_citation_network(dataset_path)
#         degree_threshold = 5
#         filtered_nodes = [node for node in citation_network.nodes if citation_network.degree(node) >= degree_threshold]
#         filtered_network = citation_network.subgraph(filtered_nodes)
#         filtered_degrees = dict(filtered_network.degree())
#         # plot(filtered_degrees, filtered_network,degree_threshold)
#         degree_dis(filtered_network)
#         # diameter(filtered_network)
#         clustering(filtered_network)
#         # connectedness(filtered_network)
#         community(filtered_network)
#         vizualisation(filtered_network)

#     except Exception as e:
#         print("Error:", str(e))


# def degree_dis(citation_network):
#         degrees = [citation_network.degree(node) for node in citation_network.nodes]
#         plt.hist(degrees, bins=20, alpha=0.7)
#         plt.title('Degree Distribution')
#         plt.xlabel('Degree')
#         plt.ylabel('Frequency')
#         plt.show()

# def diameter(citation_network):
#     diameter = nx.diameter(citation_network)
#     print(f'Graph Diameter: {diameter}')

# def centrality(citation_network):
#     degree_centrality = nx.degree_centrality(citation_network)
#     betweenness_centrality = nx.betweenness_centrality(citation_network)
#     closeness_centrality = nx.closeness_centrality(citation_network)

# def clustering(citation_network):
#     clustering_coefficient = nx.average_clustering(citation_network)
#     print(f'Average Clustering Coefficient: {clustering_coefficient}')

# def connectedness(citation_network):
#     connected_components = nx.connected_components(citation_network)
#     print(f'Number of Connected Components: {nx.number_connected_components(citation_network)}')

# def community(citation_network):
#     communities = nx.community.greedy_modularity_communities(citation_network)
#     print(f'Number of Communities: {len(communities)}')

# def vizualisation(citation_network):
#     seed = 13648
#     pos = nx.spring_layout(citation_network, seed)

#     node_dates = nx.get_node_attributes(citation_network, 'date')
#     years = [datetime.strptime(date, "%Y-%m-%d").strftime("%Y") for date in node_dates.values()]

#     unique_years = list(set(years))
#     color_map = plt.cm.get_cmap('tab10', len(unique_years))
#     node_colors = [color_map(unique_years.index(year)) for year in years]

#     plt.figure(figsize=(10, 8))
#     nx.draw(citation_network, pos, with_labels=False, node_size=50, alpha=0.7, node_color=node_colors, cmap=color_map)
    
#     legend_labels = {unique_years[i]: color_map(i) for i in range(len(unique_years))}
#     legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map(i), markersize=10) for i in range(len(unique_years))]
    
#     plt.legend(legend_handles, legend_labels.keys(), title='Years')
#     plt.title('Citation Network with Node Colors representing Years')
#     plt.show()

# if __name__ == "__main__":
#     main()
