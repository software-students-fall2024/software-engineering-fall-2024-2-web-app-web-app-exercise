# Study Buns

## Product vision statement

Our app boosts productivity by gamifying task management, offering users fun, interactive rewards for staying focused, which helps students and busy individuals stay motivated and engaged in their work.

## User stories

[User Stories](https://github.com/software-students-fall2024/2-web-app-codebuns-v2/issues)

## Steps necessary to run the software

### Set up a Python virtual environment

Here are instructions for using `pipenv`

### Using [pipenv](https://pypi.org/project/pipenv/)

Install `pipenv` using `pip`:

```
pip3 install pipenv
```

Activate it:

```
pipenv shell
```

### Or use [venv](https://docs.python.org/3/library/venv.html)

Here are instructions for using `venv`

Create a virtual environment named `.venv`:

```bash
python3 -m venv .venv
```

Activate it:

On Mac:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate.bat
```

### Install Dependencies

To install the dependencies into the currently-active virtual environment, use `pip`:

```bash
pip3 install -r requirements.txt
```

## Steps necessary for MongoDB and pynomgo

### Install pymongo

```bash
python3 -m pip install pymongo
```

### Create .env file

Create a [.env](https://knowledge.kitchen/content/courses/software-engineering/slides/flask-pymongo/#combined) to store credentials for connecting to the database.

```
MONGO_DBNAME=
MONGO_URI=

#other options
FLASK_APP="app.py"
FLASK_ENV="development"
FLASK_PORT=
SECRET_KEY=
```

### Install dotenv

Use [`dotenv`](https://pypi.org/project/python-dotenv/) retrieve the values from the [.env](https://knowledge.kitchen/content/courses/software-engineering/slides/flask-pymongo/#combined) file.

```bash
pip install python-dotenv
```

### Run the app

Start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.

## Task boards

[Sprint 1 - Task Board](https://github.com/orgs/software-students-fall2024/projects/43)
[Sprint 2 - Task Board](https://github.com/orgs/software-students-fall2024/projects/90/views/1)
