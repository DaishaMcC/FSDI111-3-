from flask import (
    Flask,
    request,
    render_template
)
import requests as pyrequests

BACKEND_URL = "http://127.0.0.1:5001"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/tasks")
def list_tasks():
    response = pyrequests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", code=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/")
def task_detail(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = pyrequests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("detail.html", task=single_task)
    return (
        render_template("error.html", code=response.status_code),
        response.status_code
    )

@app.get("/tasks/new")
def new_form():
    return render_template("new.html")

@app.post("/tasks/new")
def create_task():
    task_data = request.form
    response = pyrequests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", msg="Creation successful")
    return (
        render_template("error.html", code=response.status_code),
        response.status_code
    )
    