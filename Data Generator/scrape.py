import requests
import time

query = """SELECT ?person ?personLabel WHERE {
  ?person wdt:P31 wd:Q5.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 200000"""
start = time.time()

r = requests.get("https://query.wikidata.org/bigdata/namespace/wdq/sparql", params={'query':query, 'format':'json'})

print("Finished Request in", time.time() - start, "seconds")
with open("test.json", 'w') as f:
    f.write(r.text)
