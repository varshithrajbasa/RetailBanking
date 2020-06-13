from flask import Flask, request, render_template, redirect, request, url_for, session


app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

