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
def addNodesToDepth(graph, title, depth, centerYear):
    graph.add_node(title)

    #Node already linked in:
    if graph.out_degree[title] > 0:
        return

    #Initialize x-position:
    attributes = people_finder.get_people_referenced(title)
    graph.nodes[title]['dob'] = int(attributes['dob'])

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

    #Save to JSON at intervals
    if depth == 2:
        people_finder.save_humans_json()

NUM_CONNECTIONS = 5
def mostImportantLinks(links):
    sortedLinks = sorted(links, key=links.get, reverse=True)
    return sortedLinks[:NUM_CONNECTIONS]

#Assigns a reasonable position to all nodes
#Loop through all years, sorting them into buckets of YEAR_INTERVAL_WIDTH
#Then arrange each bucket's y position
X_INTERVAL_WIDTH = 75
YEAR_INTERVAL_WIDTH = 5
YEAR_START = 0
YEAR_END = 2020
BASE_NODE_SIZE = 30
Y_SPACING = 80
Y_MAX = 200
DEFAULT_COLOR = {'r' : 0, 'g' : 256, 'b' : 0}
def positionAllNodes(graph, centerYear):
    yearDict = {}
    for year in range(YEAR_START, YEAR_END, YEAR_INTERVAL_WIDTH):
        yearDict[year] = []

    #Add all people to year buckets:
    for title in graph.nodes:
        dob = int(graph.nodes[title]['dob'])
        print("Adding title:", title, "with dob", dob)
        yearDict[dob - (dob%5)].append(title)
    print(yearDict)
    #Position all people:
    for year in yearDict:
        i = 0
        for title in yearDict[year]:
            graph.nodes[title]['viz'] = {'size': sizeForNode(graph, title)}
            graph.nodes[title]['viz']['position'] = {'x': X_INTERVAL_WIDTH*(year//5 - centerYear//5), 'y': i*Y_SPACING}
            graph.nodes[title]['viz']['color'] = colorForYear(year)
            i = i + 1

def sizeForNode(graph, title):
    logBase = 3
    try:
        return int(BASE_NODE_SIZE*math.log(logBase*graph.in_degree(title), logBase))
    except:
        return BASE_NODE_SIZE

def colorForYear(year):
    red = int(256*(YEAR_END - year)/float(YEAR_END))
    green = int(256*(year)/float(YEAR_END))
    return {'r' : red, 'g' : green, 'b' : 0}

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

startTitle = "Taylor Swift"
addNodesToDepth(G, startTitle, 3, 0)

centerYear = int(G.nodes[startTitle]['dob'])
positionAllNodes(G, centerYear)

print("Starting node of graph", startTitle)
print("Number of nodes in graph:", G.number_of_nodes())
print("Number of edges in graph:", G.number_of_edges())
print("Time to generate graph", time.time() - start)

people_finder.save_humans_json()
nx.write_gexf(G, "../graph.gexf")
