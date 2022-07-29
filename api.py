import simplejson as json
from flask import Flask

import mysql.connector

cnx = mysql.connector.connect(user='root', password='example', host='localhost', database='airbnb')
cursor = cnx.cursor(dictionary=True)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

@app.route("/host")
def host():
    cursor.execute("SELECT * FROM host JOIN listing ON host.id = listing.host_id")
    data = cursor.fetchall()
    new_data = []
    for row in data:
        row["last_review"] = str(row["last_review"])
        new_data.append(row)
    return json.dumps(new_data)


@app.route("/location")
def location():
    cursor.execute("SELECT * FROM location JOIN listing ON location.id = listing.location_id")
    data = cursor.fetchall()
    new_data = []
    for row in data:
        row["last_review"] = str(row["last_review"])
        new_data.append(row)
    return json.dumps(new_data)


app.run()
