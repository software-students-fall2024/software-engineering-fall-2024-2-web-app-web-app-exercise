# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

This app is a comprehensive fitness tracker that empowers users at all fitness levels to create personalized workout plans, log exercise details.

## User stories

[User Stories](https://github.com/software-students-fall2024/2-web-app-code-crafters/issues/5)

## Steps necessary to run the software

### Prerequisites

Before you begin, ensure you have met the following requirements:
- **Python 3.x** is installed on your system. [Download Python](https://www.python.org/downloads/)
- **MongoDB** setup (local or MongoDB Atlas for cloud). [MongoDB Setup](https://www.mongodb.com/try/download/community)
- **Git** installed on your machine. [Download Git](https://git-scm.com/)

### Installation

#### 1. Clone the repository
To get started, clone the repository to your local machine using Git:
```bash
git clone https://github.com/software-students-fall2024/2-web-app-code-crafters.git
```

Navigate to your project directory using the `cd` command.

#### 2. Set up virtual environment
And you can create a virtual environment for the app with the command,
```bash
python3 -m venv venv
```
To activate the virtual environment named `.venv`...

On Mac:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate.bat
```

#### 3. Install dependencies
The `pip` settings file named, `requirements.txt` contains a list of dependencies - other Python modules that this app depends upon to run. Install all required Python dependencies using `pip3`:

```bash
pip3 install -r requirements.txt
```

#### 4. create a `.env` file
A file named `.env` is necessary to run the application. This file contains sensitive environment variables holding credentials such as the database connection string, username, password, etc.

An example file named `env.example` is given. Copy this into a file named `.env` and edit the values to match your database. Or, you can create a `.env` file in the root of the project directory and add the following values:

```bash
MONGO_URI="mongodb://<username>:<password>@<clustername>/myDatabase?authSource=admin&retryWrites=true&w=majority"
```

Note: You need to replace `<username>`, `<password>`, and myDatabase with your MongoDB credentials and database name.

### Run the App
To start the Flask application, run the command in your terminal:
```bash
python3 app.py
```

If you see an error about the port number being already in use, change the first `5000` in the command to a different port number, e.g. `-p 10000:5000` to use your computer's port `10000`.

View the app in your browser:

open a web browser and go to `http://localhost:5000` (or change `5000` to whatever port number you used in the command above)

## Task boards

[Task Boards](https://github.com/software-students-fall2024/2-web-app-code-crafters/projects?query=is%3Aopen)
