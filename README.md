# Web Application Exercise

## Product vision statement

A mobile-friendly web application that helps users manage their budget by tracking, searching, and organizing their spending through transaction records and balance views.

## User stories

[Link to User Stories in the Issues Page](https://github.com/software-students-fall2024/2-web-app-webstars/issues)

## Steps necessary to run the software

Before you begin, ensure you have met the following requirements:

- **Python**: This project requires Python 3.x. You can download Python from [here](https://www.python.org/downloads/).

- **Pip**: Python's package installer, `pip`, must also be installed. You can install/upgrade it by running:

  ```bash
  python -m ensurepip --upgrade
  ```

### Step 1: Clone the Repository and Navigate into project directory

To get a local copy of the project, use the following command:

```bash
git clone https://github.com/software-students-fall2024/2-web-app-webstars.git
```

Navigate into directory by running following command:

```
cd 2-web-app-webstars.git
```

**pip**
Note that most Python programs require the use of the package manager named pip - the default Python "package manager". A package manager is software that takes care of installing the correct version of any modules in the correct place for the current system you are running it on. It comes with most distributions of Python. On many machines, the Python 3-compatible version it is calld pip3 and on others it is simply pip.

### Step 2: Set up Virtual Enviroment
Install pipenv using pip:
'''
pip3 install pipenv
'''

Activate it:
'''
pipenv shell
'''

Create and activate a virtual environment using the following commands:

```
python -m venv venv
```

For macOS/Linux:

```
source venv/bin/activate
```

For Windows:

```
venv\Scripts\activate
```

### Step 3: Install Requirements

To install Flask and pymongo, run the following commands:
```
pipenv install Flask
```
```
pipenv install pymongo
```
Install the project dependencies by running the following command:
```
pip install -r requirements.txt
```

### Step 4: Create .env file

A file named .env is necessary to run the application. This file contains sensitive environment variables holding credentials such as the database connection string, username, password, etc.

For the use of this project, the env file is sent to the admins/managers via the team's messenger channel (webstars).

Once this .env file is received and downloade, place it in the root directory of the project to ensure the application runs correctly.

### Step 5: Running the software

On Mac, use the commands: 

```
export FLASK_APP=app.py
```

and

```
export FLASK_ENV=development
```

On Windows, use 

```
set FLASK_APP=app.py
```

and 

```
set FLASK_ENV=development
```

Start flask with 

```
flask run
```
This will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.


## Task boards

[Task Board Sprint 1](https://github.com/orgs/software-students-fall2024/projects/7)

[Task Board Sprint 2](https://github.com/orgs/software-students-fall2024/projects/78)


