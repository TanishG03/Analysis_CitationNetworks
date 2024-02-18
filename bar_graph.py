# import matplotlib.pyplot as plt

# # Data for each time frame
# time_frames = ['1992-1993','1993-1994','1994-1995','1995-1996', '1996-1997', '1997-1998', '1998-1999']
# nodes = [572,932,1086,1153, 1208, 1232, 1089]
# edges = [83,206,383,723, 645, 1536, 1488]

# # Plotting the bar graph for Number of Nodes
# plt.figure(figsize=(10, 5))
# plt.bar(time_frames, nodes, color='blue')
# plt.xlabel('Time Frame')
# plt.ylabel('Number of Nodes')
# plt.title('Number of Nodes Over Time')
# plt.show()

# # Plotting the bar graph for Number of Edges
# plt.figure(figsize=(10, 5))
# plt.bar(time_frames, edges, color='orange')
# plt.xlabel('Time Frame')
# plt.ylabel('Number of Edges')
# plt.title('Number of Edges Over Time')
# plt.show()

import matplotlib.pyplot as plt

# Data for the average degree values and corresponding year ranges
years = ["1993-1994", "1994-1995", "1995-1996", "1996-1997", "1997-1998", "1998-1999"]
average_degrees = [0.4463705308775731, 0.7053406998158379, 1.254119687771032, 1.0678807947019868, 2.4935064935064934, 2.7327823691460056]

# Creating a bar graph
plt.bar(years, average_degrees, color='skyblue')
plt.xlabel('Year Range')
plt.ylabel('Average Degree')
plt.title('Average Degree for Different Year Ranges (1993-1999)')
plt.ylim(0, max(average_degrees) + 0.5)  # Set y-axis limits for better visualization
plt.show()
