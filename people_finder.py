import wikipedia
import requests
import json
import time
import urllib

start_term = "Albert Einstein"

print("Loading humans.json")
start = time.time()
humans_json = json.load(open("humans.json"))
print("Loaded humans.json in", time.time() - start, "seconds")

print("Parsing humans.json")
start = time.time()
bindings = humans_json["results"]["bindings"]
humans = {}
for human in bindings:
    entity_number = human["person"]["value"][31:] #Unused
    name = human["personLabel"]["value"]
    humans[name] = entity_number
print("Parsed humans.json in", time.time() - start, "seconds")
print("There are", len(humans.keys()), "people in our database")

def get_second_degree(title):
    people = get_people_referenced(title)
    start = time.time()
    second_degree = {}
    for person in people:
        page = wikipedia.page(person)
        second_degree[person] = len(page.links)
    print("Took", time.time() - start, "seconds to find second degree")
    with open(title + '.json', 'w') as fp:
        json.dump(second_degree, fp)
    return second_degree

def get_people_referenced(title):
    start = time.time()
    page = wikipedia.page(title)
    print("Loaded Page in", time.time() - start, "seconds")
    start = time.time()
    referenced = []
    print(title, "has", len(page.links), "links")
    for link in page.links:
        if link in humans:
            referenced.append(link)
    print("Took", time.time() - start, "seconds to get", len(referenced), "referenced people.")
    return referenced, len(links_here)
