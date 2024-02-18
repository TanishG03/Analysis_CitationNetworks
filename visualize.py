# from pyvis.network import Network
# import networkx as nx
# from datetime import datetime

# def load_citation_network(file_path, date_file_path):
#     graph = nx.DiGraph()

#     # Load date information from the file
#     date_dict = {}
#     with open(date_file_path, 'r') as date_file:
#         for line in date_file:
#             if line.startswith("#"):
#                 continue
#             paper_id, date_str = line.strip().split()
#             date_dict[int(paper_id)] = date_str

#     # Load citation network from the main file
#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.startswith("#"):
#                 continue
#             source, target = map(int, line.strip().split())
#             graph.add_node(source, date=date_dict.get(source, ""))
#             graph.add_node(target, date=date_dict.get(target, ""))
#             graph.add_edge(source, target)

#     return graph

# def create_pyvis_graph(graph, degree_threshold):
#     filtered_nodes = [node for node in graph.nodes if graph.degree(node) >= degree_threshold]
#     filtered_network = graph.subgraph(filtered_nodes)

#     return filtered_network

# def main():
#     dataset_path = "./Datasets/cit-HepPh.txt/sample_100.txt"
#     date_file_path = "Datasets/cit-HepPh-dates.txt"

#     try:
#         citation_network = load_citation_network(dataset_path, date_file_path)
#         degree_threshold = 0
#         filtered_network = create_pyvis_graph(citation_network, degree_threshold)

#         # Create an interactive network visualization using pyvis
#         pyvis_graph = Network(directed=True, height="800px", width="100%", layout=True, bgcolor="#222222", font_color="white")

#         # Add nodes with date information
#         for node, data in filtered_network.nodes(data=True):
#             date_str = data.get('date', "")
#             formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d") if date_str else ""
#             label = f"{node}\nDate: {formatted_date}"
#             pyvis_graph.add_node(node, label=label, title=formatted_date)

#         # Add edges
#         for edge in filtered_network.edges():
#             pyvis_graph.add_edge(edge[0], edge[1])

#         # Manually generate HTML content
#         html_content = pyvis_graph.html
#         with open("graph.html", "w", encoding="utf-8") as html_file:
#             html_file.write(html_content)
        
#         print("HTML file saved successfully!")

#     except Exception as e:
#         print("Error:", str(e))

# if __name__ == "__main__":
#     main()


from pyvis.network import Network
import networkx as nx
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

def create_pyvis_graph(graph, degree_threshold):
    filtered_nodes = [node for node in graph.nodes if graph.degree(node) >= degree_threshold]
    filtered_network = graph.subgraph(filtered_nodes)

    return filtered_network

def main():
    dataset_path = "./Datasets/cit-HepPh.txt/sample_100.txt"
    date_file_path = "Datasets/cit-HepPh-dates.txt"

    try:
        citation_network = load_citation_network(dataset_path, date_file_path)
        degree_threshold = 0
        filtered_network = create_pyvis_graph(citation_network, degree_threshold)

        # Create an interactive network visualization using pyvis
        pyvis_graph = Network(directed=True, height="800px", width="100%", layout=True, bgcolor="#222222", font_color="white")

        # Add nodes with date information
        for node, data in filtered_network.nodes(data=True):
            date_str = data.get('date', "")
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d") if date_str else ""
            label = f"{node}\nDate: {formatted_date}"
            pyvis_graph.add_node(node, label=label, title=formatted_date)

        # Add edges
        for edge in filtered_network.edges():
            pyvis_graph.add_edge(edge[0], edge[1])

        # Save the graph directly to an HTML file
        pyvis_graph.save_graph("graph.html")
        
        print("HTML file saved successfully!")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
