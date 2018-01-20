import requests
import time
import json
import urllib.parse

base_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&titles={}"
page_links_query = "&plnamespace=0&pllimit=max"
links_here_query = "&lhprop=title&&lhnamespace=0&lhlimit=max"
prop_query = "&prop={}"


def build_request_url(title, plcontinue=None, lhcontinue=None, continuation=False, page_links_only=False):
    url = base_url.format(urllib.parse.quote(title))
    properties = []
    if not continuation: #if this is the first call, use both properties
        properties = ["links"]
        url += page_links_query
        if not page_links_only:
            properties.append("linkshere")
            url += links_here_query
    else: #if it's not the first call, use the continue values to decide whether to query for each property
        if not (plcontinue or lhcontinue):
            return None
        if plcontinue:
            properties.append("links")
            url += page_links_query
            url += "&plcontinue=" + plcontinue
        if lhcontinue and not page_links_only:
            properties.append("linkshere")
            url += links_here_query
            url += "&lhcontinue=" + lhcontinue
    url += prop_query.format(urllib.parse.quote("|".join(properties)))
    return url

def get(title, page_links_only=False):
    url = build_request_url(title, page_links_only=page_links_only)
    page_links = []
    links_here = []
    count = 1
    start = time.time()
    print("Starting request")
    def recursive_request(url):
        if not url: # Return for an empty URL
            return
        nonlocal count
        print("Making Request", count)

        agent = 'wikipedia (https://github.com/goldsmith/Wikipedia/)'
        headers = {
            'User-Agent': agent
        }
        sec_start = time.time()
        data = requests.get(url, headers=headers).json()

        # Process data
        query = data["query"]["pages"]
        query = query[list(query.keys())[0]]
        if "links" in query:
            links = query["links"]
            page_links.extend([link["title"] for link in links])
        if "linkshere" in query:
            linkshere = query["linkshere"]
            links_here.extend([link["title"] for link in linkshere])


        # Check for Continuation Details
        plcontinue, lhcontinue = None, None
        if "continue" in data:
            cont_data = data["continue"]
            if "plcontinue" in cont_data:
                plcontinue = cont_data["plcontinue"]
            if "lhcontinue" in cont_data:
                lhcontinue = cont_data["lhcontinue"]

        print("Request", count, "took", time.time() - sec_start, "seconds")
        count += 1
        new_url = build_request_url(title, plcontinue, lhcontinue, True, page_links_only)
        recursive_request(new_url)

    recursive_request(url)
    print("Finished Request in", time.time() - start, "seconds")
    print("Found", len(page_links), "page links and", len(links_here), "links here")
    return (page_links, links_here)
