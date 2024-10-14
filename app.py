import os
from flask import Flask, request, json, redirect, url_for, flash, render_template, session
from dotenv import load_dotenv

from pymongo import MongoClient
load_dotenv()  # 加载 .env 文件

# 检查 MONGO_URI 是否成功加载
mongo_uri = os.getenv('MONGO_URI')
print(f"MONGO_URI: {mongo_uri}")

# 获取 MongoDB URI
mongo_uri = os.getenv('MONGO_URI')

# 初始化 Flask 应用
app = Flask(__name__)
app.secret_key = os.urandom(13)

# 设置 MongoDB 连接
client = MongoClient(mongo_uri)
db = client['fitness_db']
todo_collection = db['todo']
exercises_collection = db['exercises']


def get_todo_list():

    todo_list = todo_collection.find_one({"_id": 1})
    if todo_list and "todo" in todo_list:
        exercises = [item['workout_name'] for item in todo_list['todo']]
        return exercises
    return []

def get_all_exercises():

    exercises = exercises_collection.find()
    return list(exercises)

def get_filtered_exercises(query: str):

    exercises = exercises_collection.find({
        "$or": [
            {"workout_name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    })
    return list(exercises)
def get_exercise_by_id(exercise_id: int):

    exercise = exercises_collection.find_one({"_id": exercise_id})
    return exercise

def add_exercise_to_todo(exercise_id: int, working_time: int, reps: int, weight: float):
    """
    向 To-Do List 中添加一个新的健身动作，包括动作名称
    """
    # 查找该动作的详细信息
    exercise = exercises_collection.find_one({"_id": exercise_id})
    
    if exercise:
        exercise_item = {
            "exercise_id": exercise_id,
            "workout_name": exercise["workout_name"],
            "working_time": working_time,
            "reps": reps,
            "weight": weight
        }

        # 查找今天的 To-Do List
        todo = todo_collection.find_one({"_id": 1})

        if todo:
            # 如果 To-Do List 已存在，更新其中的动作
            todo_collection.update_one(
                {"_id": 1},
                {"$push": {"todo": exercise_item}}
            )
        else:
            # 如果 To-Do List 不存在，创建新的计划
            todo_collection.insert_one({
                "_id": 1,
                "todo": [exercise_item]
            })
        print(f"Exercise {exercise['workout_name']} added to To-Do List.")
    else:
        print(f"Exercise with ID {exercise_id} not found.")

def delete_exercise_from_todo(exercise_id: int):
    """
    从 To-Do List 中删除指定的健身动作
    """
    todo_collection.update_one(
        {"_id": 1},
        {"$pull": {"todo": {"exercise_id": exercise_id}}}
    )
    print(f"Exercise with ID {exercise_id} deleted from To-Do List.")


def update_exercise_in_todo(exercise_id: int, working_time: int, reps: int, weight: float):
    """
    更新 To-Do List 中某个健身动作的 reps、working_time 和 weight
    """
    todo_collection.update_one(
        {"_id": 1, "todo.exercise_id": exercise_id},
        {"$set": {
            "todo.$.working_time": working_time,
            "todo.$.reps": reps,
            "todo.$.weight": weight
        }}
    )
    print(f"Exercise with ID {exercise_id} updated in To-Do List.")

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    exercise_id = int(request.form.get('exercise_id'))  # 获取动作 ID
    working_time = int(request.form.get('working_time'))
    reps = int(request.form.get('reps'))
    weight = float(request.form.get('weight'))

    add_exercise_to_todo(exercise_id, working_time, reps, weight)
    flash("Exercise added successfully!")
    return redirect(url_for('todo'))  # 重定向到 To-Do 页面

@app.route('/delete_exercise', methods=['POST'])
def delete_exercise():
    exercise_id = int(request.form.get('exercise_id'))  # 从表单获取 ID
    delete_exercise_from_todo(exercise_id)
    flash("Exercise deleted successfully!")
    return redirect(url_for('todo'))  # 重定向到 To-Do 页面

@app.route('/update_exercise', methods=['POST'])
def update_exercise():
    exercise_id = int(request.form.get('exercise_id'))  # 获取动作 ID
    working_time = int(request.form.get('working_time'))
    reps = int(request.form.get('reps'))
    weight = float(request.form.get('weight'))

    update_exercise_in_todo(exercise_id, working_time, reps, weight)
    flash("Exercise updated successfully!")
    return redirect(url_for('todo'))  # 重定向到 To-Do 页面
