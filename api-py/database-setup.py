import os
import re
import sqlite3

import requests
from lxml import etree


class Concept:
    def __init__(self, english, danish, description, source):
        self.english = english
        self.danish = danish
        self.description = description
        self.source = source

database_path = "traducir.db"

# ...connect(...) can not overwrite
if(os.path.exists(database_path)):
    os.remove(database_path)

# Create database file
value = ""
with open("sql traducir.txt") as file:
    value = file.read()

print("Creating database.")

con = sqlite3.connect(database_path)

cur = con.cursor()

# Create table with fields as described in "sql traducir.txt"
commands = value.split("\n\n")
for command in commands[:-2]:
    cur.execute(command)

# # Get values from https://topdatamat.dk/ordbog.thc
source = "https://topdatamat.dk/ordbog.thc"
parser = etree.HTMLParser()
resource = requests.get(source)
tree = etree.fromstring(resource.text, parser)

amount_concepts = len(tree.xpath("/html/body/div/article/dl/dt"))

# # Insert data into database
for i in range(1, amount_concepts):
    danish_term = tree.xpath(f"/html/body/div/article/dl/dt[{i}]")[0].text.strip()
    english_term = tree.xpath(f"/html/body/div/article/dl/dd[{i}]")[0].text.strip()
    if ("," in english_term or "eller" in english_term):
        items = re.split(r",|eller", english_term)
        items = list(map(lambda x: x.strip(), items))
        for item in items:
            value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave, Kilde) VALUES (?, ?, ?)"
            cur.execute(value, (item, danish_term, source))
    else:
        value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave, Kilde) VALUES (?, ?, ?)"
        cur.execute(value, (english_term, danish_term, source))

# # Get values from http://www.klid.dk/dansk/ordlister/ordliste.html
source = "http://www.klid.dk/dansk/ordlister/ordliste.html"
resource = requests.get(source)
tree = etree.fromstring(resource.text, parser)

terms_collection = tree.xpath("/html/body/pre[1]")[0].getchildren()

for terms in terms_collection:
    terms = terms.tail.splitlines()
    for line in terms:
        if line == "" or line is None:
            continue
        line = line.strip()
        term = line.split("\t")
        term = list(filter(None, term))
        for i in range(1, len(term)):
            english_term = term[0].strip()
            danish_term = term[i].strip()
            value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave, Kilde) VALUES (?, ?, ?)"
            cur.execute(value, (english_term, danish_term, source))

# Get values from https://imada.sdu.dk/~chdj/ordbog.php
# https://imada.sdu.dk/~chdj/ordbog_en_da.php
# file = open("sidste_side.html")
# tree = etree.parse(file, parser)
source = "https://imada.sdu.dk/~chdj/ordbog_en_da.php"
resource = requests.get(source)
tree = etree.fromstring(resource.text, parser)

# "/html/body/table/tbody/tr/td/em" if file
# reason is that browser automatically adds tbody
# "/html/body/table/tr/td/em" if request
terms_amount = len(tree.xpath("/html/body/table/tr/td/em"))

for i in range(1, terms_amount):
    term = tree.xpath(f"/html/body/table/tr/td/em[{i}]")[0]
    english_term = term.text.strip()
    regex = r"[\s:](?<!\()(?![^\(]*\))"
    danish_term = list(filter(None, re.split(regex, term.tail)))
    danish_term = " ".join(danish_term)
    value = "INSERT INTO Begreber (EngelskUdgave, DanskUdgave, Kilde) VALUES (?, ?, ?)"
    cur.execute(value, (english_term, danish_term, source))
    
# Delete duplicates in database

print("Inserting into FTS")

# Insert values into FTS table
con.commit()
for command in commands[-2:]:
    cur.execute(command)

con.commit()

con.close()

print("Succesfully created database.")
