import sqlite3
from lxml import etree


class Concept:
    def __init__(self, english, danish, description):
        self.english = english
        self.danish = danish
        self.description = description


# Get values from https://topdatamat.dk/ordbog.thc
# Replace "eller" with "or"
parser = etree.HTMLParser()
tree = etree.parse("https://topdatamat.dk/ordbog.thc", parser)

amount_concepts = len(tree.xpath("/html/body/div/article/dl/dt"))

value = ""
with open("sql traducir.txt") as file:
    value = file.read()

con = sqlite3.connect('traducir.db')

cur = con.cursor()

# Create table with fields as described in "sql traducir.txt"
cur.execute(value)
