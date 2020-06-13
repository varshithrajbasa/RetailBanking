from flask import Flask, request, render_template, redirect, request, url_for, session


app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/create_customer")
def create():
    return render_template("create_customer.html")

if __name__=="__main__":
    app.run(debug=True)