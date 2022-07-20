import json
from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)


query = "SELECT * FROM fts WHERE fts MATCH ? ORDER BY rank LIMIT 20;"
queryDisable = "UPDATE Begreber SET Aktiv = 0 WHERE Id = ?"

@app.post("/")
def searchDb():
    con = sqlite3.connect("../traducir.db")
    cur = con.cursor()
    data = request.data.decode("utf-8")
    body = f"{data}*"
    cur.execute(query, (body,))
    rows = cur.fetchall()
    con.close()
    return json.dumps(rows)

@app.delete("/")
def disableField():
    con = sqlite3.connect("../traducir.db")
    cur = con.cursor()
    id = int(request.data.decode("utf-8"))
    cur.execute(queryDisable, (id,))
    rows = cur.fetchall()
    con.commit()
    con.close()
    return f"Deleted term with id {id}"
