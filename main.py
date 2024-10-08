from flask import Flask, render_template

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

reports = ["Vending machine", "Water fountain", "Door hinge"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html", reports=reports)

if __name__ == "__main__":
    app.run()