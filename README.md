# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Job Application Tracker helps users streamline their job search process by allowing them to easily manage, track, and update their job applications, view deadlines, and perform actions like adding, editing, deleting, or searching for applications by key attributes.

## User stories

[Link to the User Stories in the Issues Page](https://github.com/software-students-fall2024/2-web-app-thecoders/issues)

## Steps necessary to run the software

Start by setting up pipenv and its specified dependencies
```
pip install pipenv
pipenv install
pipenv install flask_login
pipenv install flask_bcrypt
```

Create new file .env (will be git ignored) to hold environment variables in the following format:
```
MONGO_CONNECTION_URI=<mongo_connection_str>
```

Run the flask app
```
python app.py
```

## Task boards

[Task Board](https://github.com/orgs/software-students-fall2024/projects/22/views/1)

## Team members

* Wilson Xu [Profile](https://github.com/wilsonxu101)
* Hanna Han [Profile](https://github.com/HannaHan2)
* Sewon Kim [Profile](https://github.com/SewonKim0)
* Rhan Chen [Profile](https://github.com/xc528)