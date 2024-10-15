# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our vision is to provide an event planning platform that makes it accessible for anyone to create, manage, and execute successful events with tools for invitations and participant management, as well as provide a seamless experience for attendees to find and RSVP for events.

## User stories

[User Stories](https://github.com/software-students-fall2024/2-web-app-leodavejessalexangteamagain/issues)

## Steps necessary to run the software

### Step 1: Clone the repository
To clone the repository to your local machine, open the terminal navigate to the directory where you want to clone the repository and run the following command:
``` 
git clone https://github.com/software-students-fall2024/2-web-app-leodavejessalexangteamagain.git
``` 

### Step 2: Create a virtual environment

It is recommended to set a virtual environment with pipenv, which can be installed with the command
``` 
pip install pipenv
``` 

To activate the environment, run
``` 
pipenv shell
``` 

### Step 3: Install dependencies

To install Flask and pymongo, run the commands
``` 
pipenv install Flask
``` 
``` 
pipenv install pymongo
``` 

In the pipenv environment, run to install all dependencies. The Pipfile can alternatively used.
``` 
pipenv install -r requirements.txt
``` 

### Step 4: Set up .env file

Follow the example.env file to create a .env file in the local repository. If using Visual Studio Code, navigate the search bar and enter '>Python: Select Interpreter' and click on the virtual environment created in the previous steps.

### Step 5: Run the application

To run the application, type this command in your terminal
'''
python app.py
'''
This will output the local address where your Flask web application is running. The link can be copied and pasted to a web brower or those on Visual Studio Code can press the command key and click on the link.

## Task boards

[Sprint 1] (https://github.com/orgs/software-students-fall2024/projects/14)

[Spring 2] (https://github.com/orgs/software-students-fall2024/projects/63)
