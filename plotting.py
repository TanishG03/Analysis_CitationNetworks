# import matplotlib.pyplot as plt

# def plot_bar_graph(year_ranges, property_values, property_name):
#     plt.bar(year_ranges, property_values, alpha=0.7)
#     plt.title(f'{property_name} Across Year Ranges')
#     plt.xlabel('Year Range')
#     plt.ylabel(property_name)
#     plt.show()

# # Example usage
# year_ranges = ['1991-1992', '1992-1993', '1993-1994', '1994-1995', '1995-1996', '1996-1997', '1997-1998', '1998-1999']
# num_strongly_connected_components = [177, 572, 923, 1086, 1153, 1208, 1230, 1087]
# average_clustering_coefficient = [0.0, 0.002534965034965035, 0.003416145068366087, 0.01349251905684423, 0.023274083242573497, 0.029308938457500412, 0.0638245872810793, 0.058327818589570445]
# num_communities = [169, 496, 745, 763, 659, 777, 479, 488]
# num_nodes = [4517, 4517, 4517, 4517, 4517, 4517, 4517, 4517]
# num_edges = [10361, 10361, 10361, 10361, 10361, 10361, 10361, 10361]
# average_degree = [4.5875581137923405] * 8  # Repeat the value for each year range
# density = [0.0005079227318193467] * 8  # Repeat the value for each year range

# # Create bar graphs for each property
# plot_bar_graph(year_ranges, num_strongly_connected_components, 'Number of Strongly Connected Components')
# plot_bar_graph(year_ranges, average_clustering_coefficient, 'Average Clustering Coefficient')
# plot_bar_graph(year_ranges, num_communities, 'Number of Communities')
# plot_bar_graph(year_ranges, num_nodes, 'Number of Nodes')
# plot_bar_graph(year_ranges, num_edges, 'Number of Edges')
# plot_bar_graph(year_ranges, average_degree, 'Average Degree')
# plot_bar_graph(year_ranges, density, 'Density')
# # Add other properties as needed

import matplotlib.pyplot as plt

# # Data from the provided statistics
# years = ["1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001"]
# percent_nodes_top3 = [5.11, 4.59, 2.66, 8.84, 9.35, 15.93, 26.71, 21.03, 24.59, 38.12]

# # Plotting the bar graph
# plt.figure(figsize=(10, 6))
# plt.bar(years, percent_nodes_top3, color='skyblue')
# plt.title('Percentage of Nodes in Top 3 Communities Over the Years')
# plt.xlabel('Year')
# plt.ylabel('Percentage of Nodes in Top 3 Communities')
# plt.ylim(0, 40)  # Adjust the y-axis limit if needed
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()


# years = ["1992-1993", "1993-1994", "1994-1995","1995-1996", "1996-1997", "1997-1998", "1998-1999", "1999-2000", "2000-2001","2001-2002"]
# percent_nodes_top3 = [5.99, 7.51, 11.01, 14.45, 11.90,23.79, 21.26, 23.50, 35.70,41.40]

# # Plotting the bar graph
# plt.figure(figsize=(12, 6))
# plt.bar(years, percent_nodes_top3, color='skyblue')
# plt.title('Percentage of Nodes in Top 3 Communities for Each Year Range')
# plt.xlabel('Year Range')
# plt.ylabel('Percentage of Nodes in Top 3 Communities')
# plt.ylim(0, 40)  # Adjust the y-axis limit if needed
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()

import matplotlib.pyplot as plt

# Data from the provided statistics
# years = ["1990-1992", "1993-1995", "1994-1996", "1997-1999", "1998-2001", "2000-2002"]
# percent_nodes_top3 = [4.44, 5.99, 10.46, 23.08, 38.44, 35.53]

# # Plotting the bar graph
# plt.figure(figsize=(12, 6))
# plt.bar(years, percent_nodes_top3, color='skyblue')
# plt.title('Percentage of Nodes in Top 3 Communities for Each Year Range')
# plt.xlabel('Year Range')
# plt.ylabel('Percentage of Nodes in Top 3 Communities')
# plt.ylim(0, 45)  # Adjust the y-axis limit if needed
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()

import matplotlib.pyplot as plt

# Data for Community Statistics
years = ['1993-1995', '1994-1996', '1995-1997', '1996-1998', '1997-1999', '1998-2000', '1999-2001', '2000-2002', '2001-2003']
louvain_community_percentages = [6.46, 10.46, 15.27, 19.50, 29.53, 35.34, 55.78, 47.41, 58.34]
girvan_newman_community_percentages = [36.46, 44.46, 39.27, 57.50, 59.53, 65.34, 79.78, 77.41, 76.34]

# Bar width
bar_width = 0.35

# X-axis positions for the bars
louvain_positions = range(len(years))
girvan_newman_positions = [pos + bar_width for pos in louvain_positions]

# Plotting the grouped bar graph
plt.figure(figsize=(12, 6))

plt.bar(louvain_positions, louvain_community_percentages, width=bar_width, color='lightcoral', label='Louvain')
plt.bar(girvan_newman_positions, girvan_newman_community_percentages, width=bar_width, color='skyblue', label='Girvan-Newman')

plt.xlabel('Year Slices')
plt.ylabel('Percentage of Nodes in Top 3 Communities')
plt.title('Comparison of Louvain and Girvan-Newman Community Percentages')
plt.xticks([pos + bar_width / 2 for pos in louvain_positions], years)
plt.legend()
plt.ylim(0, 90)  # Adjust the y-axis limit if needed

plt.show()
