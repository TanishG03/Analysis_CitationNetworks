import matplotlib.pyplot as plt

def plot_bar_graph(year_ranges, property_values, property_name):
    plt.bar(year_ranges, property_values, alpha=0.7)
    plt.title(f'{property_name} Across Year Ranges')
    plt.xlabel('Year Range')
    plt.ylabel(property_name)
    plt.show()

# Example usage
year_ranges = ['1991-1992', '1992-1993', '1993-1994', '1994-1995', '1995-1996', '1996-1997', '1997-1998', '1998-1999']
num_strongly_connected_components = [177, 572, 923, 1086, 1153, 1208, 1230, 1087]
average_clustering_coefficient = [0.0, 0.002534965034965035, 0.003416145068366087, 0.01349251905684423, 0.023274083242573497, 0.029308938457500412, 0.0638245872810793, 0.058327818589570445]
num_communities = [169, 496, 745, 763, 659, 777, 479, 488]
num_nodes = [4517, 4517, 4517, 4517, 4517, 4517, 4517, 4517]
num_edges = [10361, 10361, 10361, 10361, 10361, 10361, 10361, 10361]
average_degree = [4.5875581137923405] * 8  # Repeat the value for each year range
density = [0.0005079227318193467] * 8  # Repeat the value for each year range

# Create bar graphs for each property
plot_bar_graph(year_ranges, num_strongly_connected_components, 'Number of Strongly Connected Components')
plot_bar_graph(year_ranges, average_clustering_coefficient, 'Average Clustering Coefficient')
plot_bar_graph(year_ranges, num_communities, 'Number of Communities')
plot_bar_graph(year_ranges, num_nodes, 'Number of Nodes')
plot_bar_graph(year_ranges, num_edges, 'Number of Edges')
plot_bar_graph(year_ranges, average_degree, 'Average Degree')
plot_bar_graph(year_ranges, density, 'Density')
# Add other properties as needed
