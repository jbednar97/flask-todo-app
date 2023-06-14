from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

# docker-compose up to start up the project with Docker

app = Flask(__name__, template_folder="templates")


def get_db():
    client = MongoClient(
        host='test_mongodb',
        port=27017,
        username='root',
        password='root',
        authSource='admin')
    db = client["todo_db"]
    return db


@app.route("/")
def index():
    db = get_db()
    _todos = db.todo_tb.find()
    todos = [{"task": todo["task"],
              "description":todo["description"], "done":todo["done"]} for todo in _todos]
    return render_template("index.html", todos=todos)

# Route for plain fetching todos, which will return json list of todos - unused, keeping for references
# @app.route("/todos")
# def fetch_todos():
#     db = get_db()
#     _todos = db.todo_tb.find()
#     todos = [{"task": todo["task"],
#               "description":todo["description"], "done":todo["done"]} for todo in _todos]
#     return jsonify({"todos": todos})


@app.route("/add", methods=["POST"])
def add():
    db = get_db()
    collection = db.todo_tb
    data = {
        "task": request.form["todo"],
        "description": request.form["description"],
        "done": False
    }
    collection.insert_one(data)
    return redirect(url_for("index"))


@app.route('/edit/<string:task>', methods=["GET", "POST"])
def edit(task):
    db = get_db()
    collection = db.todo_tb
    todo = collection.find_one({"task": task})
    if request.method == "POST":
        print(request.form["todo"])
        collection.update_one({"task": task}, {"$set": {
                              "task": request.form["todo"], "description": request.form["description"]}})
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo)


@app.route("/check/<string:task>")
def check(task):
    db = get_db()
    collection = db.todo_tb
    todo = collection.find_one({"task": task})
    collection.update_one({"task": task}, {"$set": {"done": not todo["done"]}})
    return redirect(url_for("index"))


@app.route("/delete/<string:task>")
def delete(task):
    db = get_db()
    collection = db.todo_tb
    collection.delete_one({"task": task})
    return redirect(url_for("index"))


@app.route("/delete-all")
def delete_all():
    db = get_db()
    collection = db.todo_tb
    collection.delete_many({})
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
