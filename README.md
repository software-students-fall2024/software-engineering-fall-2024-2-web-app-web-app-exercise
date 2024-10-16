# Study Buns

## Product vision statement

Our app boosts productivity by gamifying task management, offering users fun, interactive rewards for staying focused, which helps students and busy individuals stay motivated and engaged in their work.

## User stories

[User Stories](https://github.com/software-students-fall2024/2-web-app-codebuns-v2/issues)

## Steps necessary to run the software

### Set up a Python virtual environment

Here are instructions for using `pipenv` and running the app on Mac.

### Using [pipenv](https://pypi.org/project/pipenv/)

Install `pipenv` using `pip`:

```
pip3 install pipenv
```

Activate it:

```
pipenv shell
```

### Install Dependencies

To install the dependencies into the currently-active virtual environment, use `pip`:

```bash
pip3 install -r requirements.txt
```

### Install flask-login

```bash
pip install flask-login
```

### Run the app

- define two environment variables from the command line:
  - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
- start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.

## Task boards

[Sprint 1 - Task Board](https://github.com/orgs/software-students-fall2024/projects/43)
[Sprint 2 - Task Board]()
