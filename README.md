# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our product is a mobile web application maintenance portal where students and other NYU personnel can easily make and view repair or cleaning requests at any NYU location, while maintenance staff can have quick access to these requests and respond to them accordingly.

## User stories

We decided to focus on the following user stories when building our mobile web application:
### [Link to Issues](https://github.com/software-students-fall2024/2-web-app-yowza/issues)
- As a student, I want to be able to enter a five-digit code (from a sticker on the appliance) that will automatically tell the web app which appliance it is so that I don't have to enter all of the details about where it is manually.
- As a student/faculty, I want to submit a request so that maintenance can fix broken appliances/facilities, such as water fountains or toilets, and they can be used again.
- As a maintenance worker, I want to be able to remove appliances from the web app so that students do not try to submit requests for appliances or locations that no longer exist/have been removed.
- As a maintenance worker, I want to be able to update information about an existing appliance/location so that students can access up-to-date and correct information.
- As a maintenance worker, I want to create a new page on the portal for the new water fountain I am installing with information about its location, repair history, etc. so that I can receive work requests for that specific fountain in the future and record future repairs.
- As a maintenance worker, I want a separate interface to see a list of all requests at a glance on one screen, so that I can have an organized sense of all the issues that need to be addressed. I also want to be able to click and learn more about user-made requests.

## Steps necessary to run the software

To run the software, first clone the main branch of the git. Once on your local machine, create a virtual environment to install the right dependencies and packages. To do so, run the following in bash:
```
pip install pipenv
pipenv shell
```
Once your virtual environment is created, use `cd` to navigate to the cloned repository, then install the necessary packages by running:
```
pip install -r requirements.txt
```
You will also need to set up an `.env` file in the project to gain access to the MongoDB database. An `.env` file should be provided. Once you have done so, run `flask run`, which will start the Flask application.


## Task boards

### [Team Yowza - Sprint 1](https://github.com/orgs/software-students-fall2024/projects/41)
### [Team Yowza - Sprint 2](https://github.com/orgs/software-students-fall2024/projects/91)
