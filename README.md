# Web Application Exercise

## Product vision statement


Our app is a to-do list app that helps the user organize and keep track of their goals for a day/week/month. It includes crucial fields like date, time, requirements and name of the task or event.


## User stories

[Link to User Stories](https://github.com/software-students-fall2024/2-web-app-scoobygang/issues)

## Steps necessary to run the software
Before you begin, make sure to have python installed.

### Step 1: Clone the repository
In the terminal of your local machine, use the command: <br>
```git clone git@github.com:software-students-fall2024/2-web-app-scoobygang.git``` <br>

Then, navigate to the root of this project directory.

### Step 2: Set up an virtual environment (venv)
We ran into some issues using pipenv, so we opted for venv. To create a new virtual environment: <br>
```python -m venv .venv``` <br>

If that does not work, try: <br>
```python3 -m venv .venv```

### To activate it: 
For Mac: <br>
```source .venv/bin/activate``` <br>
<br>
For Windows: <br>
```.venv\Scripts\activate.bat``` <br>

### Step 3: Install the requirements
In your virtual environment, type the command: <br>
```pip install -r requirements.txt``` <br>

### Step 4: Create the .env file
Create a file name .env. The contents of this file is located in the scoobygang discord channel.

### Running the project
Type the command: <br>
```python app.py```

Then open a browser, and type in the url: 
```http://localhost:3000```


## Task boards

[Sprint 1 Task Board](https://github.com/orgs/software-students-fall2024/projects/16)

[Sprint 2 Task Board](https://github.com/orgs/software-students-fall2024/projects/18)
