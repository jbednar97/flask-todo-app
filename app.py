from flask import Flask, render_template, request, redirect ,url_for

app = Flask(__name__,template_folder="templates")

todos = [{"task":"Create application", "description":"Application should be made in Flask, and have CRUD operations.", "done":True},{"task":"Get a review", "description":"Find out if this application matches expectations", "done":False}]

@app.route("/")
def index():
    return render_template("index.html", todos = todos)


@app.route("/add", methods=["POST"])
def add():
    todo = request.form["todo"]
    description = request.form['description']
    todos.append({"task": todo, "description": description, "done": False})
    return redirect(url_for("index"))


@app.route('/edit/<int:index>', methods=["GET","POST"])
def edit(index):
    todo = todos[index]
    if request.method == "POST":
        todo['task'] = request.form["todo"]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html",todo=todo,index=index)


@app.route("/check/<int:index>")
def check(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))

@app.route("/delete-all")
def delete_all():
    todos.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)