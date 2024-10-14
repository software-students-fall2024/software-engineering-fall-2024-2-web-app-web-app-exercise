from pymongo import MongoClient

# 连接 MongoDB，并禁用 SSL 证书验证
client = MongoClient("mongodb+srv://haoyiwang1127:wR4x7SonEN3U0lF8@cluster0.0yolx.mongodb.net/fitness_db?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client['fitness_db']
todo_collection = db['todo']

# 更新 To-Do 列表中的每个项目，添加 exercise_todo_id
todos = todo_collection.find()

for todo in todos:
    todo_id = todo['_id']
    for index, exercise in enumerate(todo['todo']):
        exercise_todo_id = index + 1  # 为每个 exercise_todo_id 赋值

        # 使用 $set 更新数据库中的 exercise_todo_id
        todo_collection.update_one(
            {"_id": todo_id, "todo.exercise_id": exercise['exercise_id']},
            {"$set": {"todo.$.exercise_todo_id": exercise_todo_id}}
        )

        print(f"Updated exercise with exercise_id {exercise['exercise_id']} in To-Do list {todo_id}, set exercise_todo_id to {exercise_todo_id}")

print("Database update completed.")
