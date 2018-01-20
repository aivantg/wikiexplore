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

#def twoStepConnections(graph, start, end):

startTitle = "Antonie Pannekoek"
start = time.time()
G = nx.DiGraph()
addNodesToDepth(G, startTitle, 2)
print("Starting node of graph", startTitle)
print("Number of nodes in graph:", G.number_of_nodes())
print("Number of edges in graph:", G.number_of_edges())
print("Time to generate graph", time.time() - start)
#addNodeWithLinks(G, startPage.title, startPage.links)

#Write the graph
nx.write_multiline_adjlist(G, "graphAdjList")
#nx.write_multiline_adjlist(G, "/dev/stdout")
