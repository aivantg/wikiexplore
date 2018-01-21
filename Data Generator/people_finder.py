import wikipedia
import requests
import json
import time
import urllib

print("Loading humans.json")
start = time.time()
with open("../humans.json", "r") as jsonFile:
    humans = json.load(jsonFile)
print("Loaded humans.json in", time.time() - start, "seconds")


def get_people_referenced(title):
    current = humans[title]
    if current: #if it's not an empty array
        return current

    page = wikipedia.page(title)

    referenced = {}
    for link in page.links:
        if link in humans:
            score = get_score(link, page.content)
            if score > 0:
                referenced[link] = score
    humans[title] = referenced
    return referenced

def get_score(name, text):
    score = 0
    names = name.split(" ")
    last_name = None
    if len(names) == 2:
        last_name = names[1]
    score += text.count(" " + name + " ")
    if last_name:
        score += ((text.count(" " + last_name + " ") - score)*0.5)
    return score



def save_humans_json():
    with open("../humans.json", 'w') as f:
        json.dump(humans, f)
