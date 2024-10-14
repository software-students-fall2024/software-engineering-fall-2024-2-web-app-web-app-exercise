# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

### Project structure (10/14/2024)

```text
.
├── LICENSE
├── Models.py
├── README.md
├── __pycache__
│   └── Models.cpython-310.pyc
├── app.py
├── exercise_data.json
├── food_data.txt
├── images
│   ├── ankle_circles.gif
│   ├── ...
├── instructions.md
├── requirements.txt
├── static
│   ├── add-button.png
│   ├── css
│   │   ├── calories.css
│   │   ├── index_style.css
│   │   ├── my_weekly_report_style.css
│   │   └── style.css
│   ├── delete-button.png
│   ├── icon.svg
│   └── trash-fill.svg
├── templates
│   ├── auth.html
│   ├── details.html
│   ├── food_instruction.html
│   ├── index.html
│   ├── my_weekly_report.html
│   ├── script.js (this file should be moved to /static)
│   └── workout_instruction.html
└── utils
    ├── exercise_db.py
    └── food_db.py
```

### Idea of User structure (db["usr"] collection) - updated in 10/13/2024, test day on Sun
```json
[
    {
        "_id": {
            "$oid": "670c941221e2684be29679f6"
        },
        "user_name": "imyhalex",
        "password": "imyhalex",
        "height": {
            "feet": 5,
            "inches": 7
        },
        "weekly_values": [
            {
                "weekly_weight": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    133
                ],
                "weekly_calorie": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    105.9
                ],
                "weekly_bmi": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    20.8
                ],
                "weekly_protein": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0.5
                ],
                "weekly_carbs": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    28.1
                ],
                "weekly_fats": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0.3
                ],
                "weekly_sugar": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    20.6
                ]
            }
        ],
        "daily_workout_plan": [
            {
            "name": "seated side crunch (wall)",
            "setNum": 2,
            "gif_path": "images/seated_side_crunch_wall.gif",
            "target_muscle": "abs",
                "timer": {
                    "duration": 0,
                    "status": "stopped"
                }
            },
            {
            "name": "band vertical pallof press",
            "setNum": 5,
            "gif_path": "images/band_vertical_pallof_press.gif",
            "target_muscle": "abs",
                "timer": {
                    "duration": 0,
                    "status": "stopped"
                }
            }
        ]
    },
    {
        ...
        ...
    }
]
```
### Idea of Food Nutrition structure (db["food"] collection structure)
```json
[
    {
        "food_name": "Bread"
        , "category": "carbs"
        , "query_name": "bread"
    },
    {
        ...
        ...
    }
]
```
### Idead of exercise structure (db["exercise"] collection structure)
```json
[
    {
        "categories": "waist",
        "equipment": "body weight",
        "gif_path": "images/flag.gif",
        "id": "3303",
        "name": "flag",
        "target_muscle": "abs",
        "secondaryMuscles": [
            "obliques",
            "shoulders"
        ],
        "instructions": [
            "Start by gripping a vertical pole with both hands, palms facing each other, and arms fully extended.",
            "Engage your core and lift your legs off the ground, keeping them straight.",
            "Using your core and upper body strength, raise your legs until they are parallel to the ground.",
            "Hold this position for as long as you can, maintaining a straight body line.",
            "Slowly lower your legs back down to the starting position.",
            "Repeat for the desired number of repetitions."
        ]
    },
    {
        ...
        ...
    }
]
```

## Product vision statement

The vision behind our application is simple: to simplify the journey towards personal health and fitness. So our vision statement can be:

> Our app empowers users to achieve their fitness goals by providing a platform that not only guides through workout plans but also tracks dietary calorie intake.

## User stories

___Workout Tracking___

- As a `user`, I want to browse exercises by muscle group so that I can focus on specific areas during my workout.
- As a `user`, I want to see animated GIFs and instructions for each exercise so that I can perform them correctly.

___Dietary Calorie Tracking___

- As a `user`, I want to search for food items and see their nutritional information so that I can track my calorie intake accurately.
- As a `user`, I want to add my daily meals to the app so that I can see how many calories I have consumed throughout the day.

___Personal Progress___

- As a `user`, I want to input my daily weight and height so that I can track my BMI and monitor my progress.
- As a `user`, I want to see a weekly report of my calorie intake and body weight so that I can evaluate my health progress over time.

## Steps necessary to run the software

___1. Maker sure MongodDB is installed in your computer___
> - [link to download the mongodb](https://www.mongodb.com/try/download/community)
> - You shold download the commity server, mongo shell, and the mongodb compass based on your computer's operation system

___2. Clone this repository to your local machine___
```text
https://github.com/software-students-fall2024/2-web-app-garage1.git
```

___3. Start and make sure your mongodb is working in terminal(Linux/MacOS)___
```bash
$ sudo systemctl start mongod
$ sudo systemctl status mongod
```
___4. Open the workspace, create a new virtual with the name `.venv`___
```shell
$ python3 -m venv .venv
```

___5. Ensure your `.venv` and `.env` is included within the `.gitignore`___

___6. Ensure your `.env` contains your localhost databse and API keys___
```text
# MongoDB Configuration
MONGO_URI=YOUR_MONGODB_URI

# Api Key
API_NINJAS_KEY=3/8OcZmswlIcnvOJgeDsig==wroCzK0qvIl8W7XM (copy this directly to the file)
```
___7. In the terminal, enter these two command to seed the data respectively___
```bash
$ python utils/food_db.py
$ python utils/exercise_db.py
```
___8. Run the application___
```bash
$ python app.py
```

## Task boards

- [Task board1 for our team](https://github.com/orgs/software-students-fall2024/projects/6)
- [Task board2 for our team](https://github.com/orgs/software-students-fall2024/projects/21/views/1)
