# Study Buns

## Product vision statement

Our app boosts productivity by gamifying task management, offering users fun, interactive rewards for staying focused, which helps students and busy individuals stay motivated and engaged in their work.

## User stories

[User Stories](https://github.com/software-students-fall2024/2-web-app-codebuns-v2/issues)

## Steps necessary to run the software

### Clone the repository

```
git clone https://github.com/software-students-fall2024/2-web-app-codebuns-v2.git
```

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

Create a [.env](https://knowledge.kitchen/content/courses/software-engineering/slides/flask-pymongo/#combined) to store credentials for connecting to the database. This file should be excluded from version control in the [`.gitignore`](.gitignore) file.

Replace the example values with values that match your database credentials.

```
MONGO_DBNAME=example
MONGO_URI="mongodb://admin:secret@localhost:27017/example?authSource=admin&retryWrites=true&w=majority"

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

- define two environment variables from the command line:
  - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
- in some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=5000` (or change to `python -m ...` if the `python3` command is not found on your system).

## Task boards

[Sprint 1 - Task Board](https://github.com/orgs/software-students-fall2024/projects/43)
[Sprint 2 - Task Board](https://github.com/orgs/software-students-fall2024/projects/90/views/1)
