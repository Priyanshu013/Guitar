import os

from flask import Flask, render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine= create_engine("postgres://postgres:mamtajain123@localhost:5432")
db= scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights=db.execute("select * from flights").fetchall()
    return render_template("index.html",flights=flights)

@app.route("/book",methods=["POST"])
def book():
    """Book a flight."""

    name=request.form.get("name")
    try:
        flight_id=int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html",message="Invalid Flight Number.")

    if db.execute("select * from flights where id=:id",{"id": flight_id}).rowcount==0:
        return render_template("error.html",message="No such flight found")
    db.execute("insert into passengers (name,flight_id) values (:name,:flight_id)",{"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")
