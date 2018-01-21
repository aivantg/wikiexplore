import wikipedia
import requests
import json
import time
import re

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

    attributes = {}
    attributes["referenced"] = referenced
    attributes["dob"] = get_date(page.content)
    humans[title] = attributes
    return attributes

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

def get_date(text):
    simpleRegex = r"[0-9]{4}"
    match = re.search(simpleRegex, text)
    if not match:
        simpleRegex = r"[0-9]{3}"
        match = re.search(simpleRegex, text)
    if not match:
        return 1000
    return match.group()

def clear_humans():
    with open("../humans.json", "r") as jsonFile:
        humans = json.load(jsonFile)

    for key in list(humans.keys()):
        humans[key] = {}

    with open("../humans.json", 'w') as f:
        json.dump(humans, f)


def save_humans_json():
    with open("../humans.json", 'w') as f:
        json.dump(humans, f)
