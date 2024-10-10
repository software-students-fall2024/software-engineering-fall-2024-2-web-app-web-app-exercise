# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

### Project structure (10/10/2024)

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
│   └── css
│       ├── index_style.css
│       ├── my_weekly_report_style.css
│       └── style.css
├── templates
│   ├── details.html
│   ├── index.html
│   ├── my_weekly_report.html
│   ├── script.js
│   ├── workout_instruction.html
│   └── workout_plan.html
└── utils
    ├── exercise_db.py
    └── food_db.py

```

### Idea of User structure
```json
[
    {
        "user_name": ""
        , "password": ""
        , "height": ""
        , "weekly_values":[ # i am planning to track multiple weeks (such as previous 2 weeks), and let user decide whether to delete it
            {
                "weekly_weight":[]
                , "weekly_calorie":[]
                , "weekly_bmi":[]
            },
            {
                ...
                ...
            }
        ]
        , "workout_palns": []
    },
    {
        ...
        ...
    }
]
```
### Idea of Food Nutrition structure
```json
[
    {
        "food_name": "Bread"
        , "category": ""
        , "query_name": "bread" + variable
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

See instructions. Delete this line and place instructions to download, configure, and run the software here.

## Task boards

- [Task board1 for our team](https://github.com/orgs/software-students-fall2024/projects/6)
- [Task board2 for our team](https://github.com/orgs/software-students-fall2024/projects/21/views/1)
