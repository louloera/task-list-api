from flask import Blueprint,jsonify, make_response,request
from app import db
from app.models.task import Task
import datetime
import os
from dotenv import load_dotenv
#from slack_sdk import WebClient
from app.routes.routes import handle_id_request
import requests 


tasks_bp = Blueprint ("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except: 
        return make_response({"details": "Invalid data"},400)
    
    db.session.add(new_task)
    db.session.commit()
    task_response = new_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 201)


@tasks_bp.route("", methods=[ "GET"])
def read_all_tasks():

    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sorting_query=="desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    
    for task in tasks: 
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify (tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):

    task=handle_id_request(Task, task_id)
    task_response = task.to_dict()
    return make_response({"task": task_response},200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)
    request_body = request.get_json()
    updated_task.title = request_body["title"]
    updated_task.description = request_body["description"]
    db.session.commit()
    task_response = updated_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 200)

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):

    task= handle_id_request(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'},200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def finished_task(task_id):

    updated_task=handle_id_request(Task, task_id)
    updated_task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    
    #slack_token = os.environ["SLACK_BOT_TOKEN"]

    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_BOT_TOKEN")
    data ={ "channel": "task-notifications",
           "text":f"Someone just completed a task {updated_task.title}",
           "token": token
    }

    response = requests.post(url, data=data)

    # result = client.chat_postMessage(
    #     channel="task-notifications", 
    #     text=f"Someone just completed the task {updated_task.title}"
    # )

    task_response = updated_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 200)



@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def unfinished_task(task_id):

    updated_task=handle_id_request(Task, task_id)
    updated_task.completed_at = None
    db.session.commit()
    task_response = updated_task.to_dict()
    
    return make_response(jsonify ({"task":task_response}), 200)
