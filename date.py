import wikipedia
import re

def dateOfBirth(title):
    page = wikipedia.page(title)
    content = page.content

    #Janky: Regex to get the first 3 or 4 digit number in content
    yearRegex = r"[0-9]{3}|[0-9]{4}"
    simpleRegex = r"[0-9]{4}"
    match = re.search(simpleRegex, content)
    if not match:
        print("No year match in article")
    else:
        print("Year match: ", match.group())
