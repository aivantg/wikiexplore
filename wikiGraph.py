import people_finder
import networkx as nx
import time

#Adds a node to the graph with given title, edges from node to links
def addNodeWithLinks(graph, title, links):
    graph.add_node(title)
    for link in links:
        graph.add_edge(title, link)

#Branch out from a given person to construct a graph of given depth
def addNodesToDepth(graph, title, depth):
    #print("Adding node for ", title)
    if depth <= 0:
        return
    links = people_finder.get_people_referenced(title)
    for link in links:
        graph.add_edge(title, link)
        if graph.out_degree[link] == 0:
            addNodesToDepth(graph, link, depth - 1)

#Returns number of two step paths from start to end
def numTwoStepPaths(graph, start, end):
    if (start not in G) or (end not in G):
        return 0
    print("Start:", start, "End:", end)
    startTime = time.time()
    undirected = graph.to_undirected()
    paths = nx.all_simple_paths(undirected, start, end, 2)
    print("Time to count two step paths between ", start, "and ", end, "is:", time.time() - startTime)
    return len(list(paths))

#Calculate what we think the edge weight should be from start to end, using links
#Returns 0 if there is no link from start to end
def calcEdgeWeight(graph, start, end):
    if not graph.has_edge(start, end):
        return 0.0
    totalDegree = graph.in_degree(end) + graph.out_degree(end) + graph.in_degree(start) + graph.out_degree(start)
    return float(numTwoStepPaths(graph, start, end))/log(totalDegree)

start = time.time()
G = nx.DiGraph()

startTitle = "Carol Shea-Porter"

addNodesToDepth(G, startTitle, 2)
print("Starting node of graph", startTitle)
print("Number of nodes in graph:", G.number_of_nodes())
print("Number of edges in graph:", G.number_of_edges())
print("Time to generate graph", time.time() - start)

endTitle = "Antonie Pannekoek"
print("Num 2-step paths between", startTitle, "and", endTitle, "is: ", numTwoStepPaths(G, startTitle, endTitle))

for link in G.neighbors(startTitle):
    G.edges[startTitle,link]['weight'] = calcEdgeWeight(G, startTitle,link)

people_finder.save_humans_json()

#nx.write_gexf(G, "graph.gexf")

import matplotlib.pyplot as plt
values = [0.25 for node in G.nodes()]


black_edges = [edge for edge in G.edges()]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       node_color = values, node_size = 5)
#nx.draw_networkx_labels(G, pos, fontsize=4)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True, width=0.2)
plt.show()


#Write the graph
#nx.write_multiline_adjlist(G, "graphAdjList")
#nx.write_multiline_adjlist(G, "/dev/stdout")
