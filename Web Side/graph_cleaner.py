with open("graph.gexf", "r") as myFile:
    data = myFile.read()

data = data.replace(" r=\"", "[tempvar]")
data = data.replace(" b=\"", " r=\"")
data = data.replace("[tempvar]", " b=\"")

with open("graph.gexf", "w") as myFile:
    myFile.write(data)
