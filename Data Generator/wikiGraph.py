import people_finder
import networkx as nx
import time
import math
import random

#Adds a node to the graph with given title, edges from node to links
def addNodeWithLinks(graph, title, links):
    graph.add_node(title)
    for link in links:
        graph.add_edge(title, link)

#Branch out from a given person to construct a graph of given depth
def addNodesToDepth(graph, title, depth):
    graph.add_node(title)
    graph.nodes[title]['viz'] = {'size': 20} #can scale by inbound nodes
    graph.nodes[title]['viz']['position'] = {'x': random.randint(-100, 100), 'y': random.randint(-100, 100)}
    graph.nodes[title]['viz']['color'] = {'r' : 0, 'g' : 256, 'b' : 0}
    if depth <= 0:
        return
    attributes = people_finder.get_people_referenced(title)
    graph.nodes[title]['dob'] = attributes['dob']
    links = attributes["referenced"]
    for person in links:
        graph.add_edge(title, person)
        if graph.out_degree[person] == 0:
            addNodesToDepth(graph, person, depth - 1)

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
    return float(numTwoStepPaths(graph, start, end))/math.log(totalDegree)

start = time.time()
G = nx.DiGraph()

startTitle = "Carol Shea-Porter"

addNodesToDepth(G, startTitle, 3)
print("Starting node of graph", startTitle)
print("Number of nodes in graph:", G.number_of_nodes())
print("Number of edges in graph:", G.number_of_edges())
print("Time to generate graph", time.time() - start)

for link in G.neighbors(startTitle):
    G.edges[startTitle,link]['weight'] = calcEdgeWeight(G, startTitle,link)

people_finder.save_humans_json()
nx.write_gexf(G, "../graph.gexf")
