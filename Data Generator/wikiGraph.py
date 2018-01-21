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
#Adds vizualization attributes for each node along the way
yMax = 350
xScaleFactor = 15
def addNodesToDepth(graph, title, depth, centerYear):
    graph.add_node(title)

    #Node already linked in:
    if graph.out_degree[title] > 0:
        return

    #Initialize node otherwise:
    graph.nodes[title]['viz'] = {'size': 20}
    graph.nodes[title]['viz']['color'] = {'r' : 0, 'g' : 256, 'b' : 0}

    #Initialize x-position:
    attributes = people_finder.get_people_referenced(title)
    dob = int(attributes['dob'])
    graph.nodes[title]['dob'] = dob
    if centerYear == 0:
        centerYear = dob
    graph.nodes[title]['viz']['position'] = {'x': xScaleFactor*(dob - centerYear), 'y': yMax*random.uniform(-1.0, 1.0)}

    #If node is a leaf node:
    if depth <= 0:
        return

    #Otherwise Link node into graph, update attributes
    links = attributes["referenced"]
    importantLinks = mostImportantLinks(links)
    for person in importantLinks:
        graph.add_edge(title, person, weight = links[person])
        if graph.out_degree[person] == 0:
            addNodesToDepth(graph, person, depth - 1, centerYear)

numConnections = 5
def mostImportantLinks(links):
    sortedLinks = sorted(links, key=links.get, reverse=True)
    return sortedLinks[:numConnections]

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

startTitle = "Abby Wambach"
addNodesToDepth(G, startTitle, 3, 0)
print("Starting node of graph", startTitle)
print("Number of nodes in graph:", G.number_of_nodes())
print("Number of edges in graph:", G.number_of_edges())
print("Time to generate graph", time.time() - start)

people_finder.save_humans_json()
nx.write_gexf(G, "../graph.gexf")
