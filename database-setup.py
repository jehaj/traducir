import sqlite3
from lxml import etree
import requests
import os
import re


class Concept:
    def __init__(self, english, danish, description):
        self.english = english
        self.danish = danish
        self.description = description


database_path = "traducir.db"


if(os.path.exists(database_path)):
    os.remove(database_path)

# Create database file
value = ""
with open("sql traducir.txt") as file:
    value = file.read()

con = sqlite3.connect(database_path)

cur = con.cursor()

# Create table with fields as described in "sql traducir.txt"
cur.execute(value)

# Get values from https://topdatamat.dk/ordbog.thc
# Replace "eller" with "or"
parser = etree.HTMLParser()
resource = requests.get("https://topdatamat.dk/ordbog.thc")
tree = etree.fromstring(resource.text, parser)

amount_concepts = len(tree.xpath("/html/body/div/article/dl/dt"))

# Insert data into database
for i in range(1, amount_concepts):
    danish_term = tree.xpath(f"/html/body/div/article/dl/dt[{i}]")[0].text.strip()
    english_term = tree.xpath(f"/html/body/div/article/dl/dd[{i}]")[0].text.strip()
    if ("," in english_term or "eller" in english_term):
        items = re.split(r",|eller", english_term)
        items = list(map(lambda x: x.strip(), items))
        for item in items:
            value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave) VALUES (?, ?)"
            cur.execute(value, (item, danish_term))
    else:
        value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave) VALUES (?, ?)"
        cur.execute(value, (english_term, danish_term))

con.commit()

con.close()