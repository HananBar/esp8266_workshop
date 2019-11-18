from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from db_access import WorkshopDb
from task01_connect import Task01_Connect
from task02_static import Task02_StaticIp
from task03_webserver import Task03_WebServer
from task04_api import Task04_ApiResponse
from task05_temperature import Task05_ApiResponse
from task06_time import Task06_ApiResponse
from task07_lights import Task07_Lights
from task08_tv import Task08_TvControl
from task09_ac import Task09_AcControl
from task10_screen import Task10_Screen

app = Flask(__name__)
CORS(app)
db_client = MongoClient('mongodb://localhost:27017/')
db_handle = db_client['esp8266_workshop']
groups_collection = db_handle['groups']
tasks_collection = db_handle['tasks']
tasks_classes = [
    Task01_Connect,
    Task02_StaticIp,
    Task03_WebServer,
    Task04_ApiResponse,
    Task05_ApiResponse,
    Task06_ApiResponse,
    Task07_Lights,
    Task08_TvControl,
    Task09_AcControl,
    Task10_Screen
]
tasks_objects = [t() for t in tasks_classes]


@app.route('/')
def api_root():
    return 'Flask Online'


@app.route('/tasks')
def api_tasks():
    tasks = []
    groups = []
    all_tasks = tasks_collection.find({}, {'_id': 0})  # find all tasks omit _id
    for t in all_tasks:
        tasks.append(t)
    all_groups = groups_collection.find({}, {'_id': 0})  # find all groups omit _id
    for g in all_groups:
        groups.append(g)
    for task in tasks:
        group_number = task['completed_by']
        if group_number != '':
            first_in_task = groups[group_number-1]['name'].__str__()
            if first_in_task != '':
                task['completed_by'] = first_in_task + ' (Group ' + group_number.__str__() + ')'
    resp = jsonify({'tasks': tasks})
    resp.status_code = 200
    return resp


@app.route('/groups')
def api_groups():
    groups = []
    all_groups = groups_collection.find({}, {'_id': 0}) # find all groups omit _id
    for g in all_groups:
        groups.append(g)
    resp = jsonify({'groups':groups})
    resp.status_code = 200
    return resp


@app.route('/group/<group_id>')
def api_group(group_id):
    group = groups_collection.find({'number': int(group_id)}, {'_id': 0})
    resp = jsonify(group[0])
    resp.status_code = 200
    return resp


@app.route('/test/<task_id>', methods=['POST'])
def api_test(task_id):
    data = request.form
    group_id = int(data['group_id'])
    points = int(data['points'])
    if int(task_id) <= len(tasks_objects):
        status = 'passed' if tasks_objects[int(task_id) - 1].test(group_id, points) else 'failed'
        group = groups_collection.find({'number': group_id}, {'_id': 0})
        msg = group[0]['dbg_msg']
    else:
        status = 'failed'
        msg = 'wrong task number'
    resp = jsonify({'status': status,
                    'message': msg})
    resp.status_code = 200
    return resp


@app.route('/skip/<task_id>', methods=['POST'])
def api_skip(task_id):
    data = request.form
    group_id = int(data['group_id'])
    if int(task_id) <= len(tasks_objects):
        tasks_objects[int(task_id) - 1].group_completed(group_id, 5)
        group = groups_collection.find({'number': group_id}, {'_id': 0})
        msg = group[0]['dbg_msg']
        resp = jsonify({'status': 'passed',
                        'message': msg})
    else:
        resp = jsonify({'status': 'failed',
                        'message': 'wrong task number'})
    resp.status_code = 200
    return resp


@app.route('/bonus/<bonus_id>', methods=['POST'])
def api_bonus(bonus_id):
    data = request.form
    group_id = int(data['group_id'])
    points = int(data['points'])
    if int(bonus_id) <= 2:
        db = WorkshopDb()
        db.group_add_bonus(group_id, points, f'Bonus task {bonus_id} completed. adding {points} points')
        group = groups_collection.find({'number': group_id}, {'_id': 0})
        msg = group[0]['dbg_msg']
        resp = jsonify({'status': 'passed',
                        'message': msg})
    else:
        resp = jsonify({'status': 'failed',
                        'message': 'wrong bonus number'})
    resp.status_code = 200
    return resp


@app.route('/reload_yaml')
def api_reload_yaml():
    print('Reloading yaml')
    db = WorkshopDb()
    db.reload_yaml()
    resp = jsonify({'status': 'success'})
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    # start the server
    app.run(debug=False, host="0.0.0.0")
