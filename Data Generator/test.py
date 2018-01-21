import requests
import json
import people_finder
import birth
import wikipedia

person = "Jesus"
ref = people_finder.get_people_referenced(person)
names = sorted(ref, key=ref.__getitem__, reverse=True)

for name in names:
    dateOfBirth = birth.dateOfBirth(name)
    print(name, "was born in", dateOfBirth)
