import wikipedia
import requests
import json
import time
import urllib

print("Loading humans.json")
start = time.time()
with open("humans.json", "r") as jsonFile:
    humans = json.load(jsonFile)
print("Loaded humans.json in", time.time() - start, "seconds")

#print("Parsing humans.json")
start = time.time()

#print("Parsed humans.json in", time.time() - start, "seconds")
#print("There are", len(humans.keys()), "people in our database")

def time_test(title):
    start = time.time()
    data = get_people_referenced(title)
    print("Took", time.time() - start, "seconds")

def get_people_referenced(title):
    if title not in humans:
        return []
    current = humans[title]
    if current:
        #print("Returned Cached Values")
        return current
    #start = time.time()
    page = wikipedia.page(title)
    #print("Loaded Page in", time.time() - start, "seconds")
    start = time.time()
    referenced = []
    #print(title, "has", len(page.links), "links")
    for link in page.links:
        if link in humans:
            referenced.append(link)
    #print("Took", time.time() - start, "seconds to get", len(referenced), "referenced people.")
    humans[title] = referenced
    return referenced

def save_humans_json():
    with open("humans.json", 'w') as f:
        json.dump(humans, f)
