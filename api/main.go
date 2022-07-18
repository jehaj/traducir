package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	_ "modernc.org/sqlite"
)

type row struct {
	Term   string
	Begreb string
	Kilde  string
	Id     int
	Aktiv  bool
}

const port int = 8005
const query string = "SELECT EngelskUdgave, DanskUdgave, Kilde, Id, Aktiv FROM Begreber WHERE (EngelskUdgave LIKE ? OR DanskUdgave LIKE ?) AND Aktiv IS 1;"

var db *sql.DB
var err error
var stmt *sql.Stmt

func apiHandler(w http.ResponseWriter, req *http.Request) {
	if req.Method == "POST" {
		post(req, w)
	} else if req.Method == "DELETE" {
		delete(req, w)
	}
}

func post(req *http.Request, w http.ResponseWriter) {
	b, _ := ioutil.ReadAll(req.Body)
	body := string(b)
	log.Print(body)
	body = fmt.Sprintf("%%%s%%", body)

	rows, _ := stmt.Query(body, body)
	defer rows.Close()
	got := []row{}
	for rows.Next() {
		var r row
		err = rows.Scan(&r.Term, &r.Begreb, &r.Kilde, &r.Id, &r.Aktiv)
		if err != nil {
			if err != sql.ErrNoRows {
				log.Fatalf("Scan: %v", err)
			}
		}
		got = append(got, r)
	}

	j, _ := json.Marshal(got)
	w.Header().Add("Content-Type", "application/json")
	w.Write(j)
}

func delete(req *http.Request, w http.ResponseWriter) {

}

func main() {
	db, err = sql.Open("sqlite", "../traducir.db")
	stmt, _ = db.Prepare(query)
	if err != nil {
		log.Fatalf("Cannot open database. Make sure it is created: %v", err)
	}

	http.HandleFunc("/", apiHandler)
	var address string = fmt.Sprintf(":%v", port)
	log.Printf("Listening at http://localhost:%v", port)
	log.Fatal(http.ListenAndServe(address, nil))
}
