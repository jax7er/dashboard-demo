import re

import psycopg2 as pg
from flask import Flask, redirect, render_template, request
from werkzeug import Response

app = Flask(__name__)

error = None
conn_config = dict(
    host="tyke.db.elephantsql.com",
    database="esvuwiyz",
    user="esvuwiyz",
    password="Qg3nCkxxgp2fneMVZqUwEnSYuEGQiWlc",
)


@app.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    global error
    
    if not error:
        if request.method == "POST":
            if username := request.form.get("username", "").lower():
                return redirect(f"/dashboard/{username}")
            else:
                error = "Username is blank"
    
    try:
        return render_template("index.j2", error=error)
    finally:
        error = None


@app.route("/dashboard/<string:username>")
def dashboard(username: str) -> Response | str:
    global error

    time_ = data = None

    if not error:
        with pg.connect(**conn_config) as conn, conn.cursor() as cur:
            try:
                cur.execute(f"SELECT time, data FROM {username} ORDER BY time DESC LIMIT 1;")
            except Exception as e:
                error = str(e)
                if re.match(r"relation \".+\" does not exist", error):
                    error = f"User {username} does not exist"
                return redirect("/")
            else:
                if result := cur.fetchone():
                    time_, data = result
                else:
                    error = "No result from fetch"
    
    try:
        return render_template("dashboard.j2", 
            error=error,
            username=username,
            datetime=str(time_),
            data=data,
        )
    finally:
        error = None
