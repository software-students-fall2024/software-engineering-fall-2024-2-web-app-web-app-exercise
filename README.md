# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Job Application Tracker helps users streamline their job search process by allowing them to easily manage, track, and update their job applications, view deadlines, and perform actions like adding, editing, deleting, or searching for applications by key attributes.

## User stories

1. As a job seeker, I want to add new job applications so that I can keep track of new opportunities that interest me.
2. As a job seeker, I want to edit my job application details so that I can update information like the stage or deadlines as I progress through the application process.
3. As a job seeker, I want to delete job applications so that I can remove applications for jobs I'm no longer interested in or those that are no longer relevant.
4. As a job seeker, I want to search applications by job title, company, location, or stage so that I can quickly find specific applications I have previously saved.
5. As a job seeker, I want to view a list of all my job applications with deadlines so that I can prioritize applications based on approaching deadlines.
6. As a job seeker, I want to access the link to the job description directly from the application so that I can quickly revisit the job posting for more details.
7. As a job seeker, I want to track the current stage of my job applications so that I can know where I am in the hiring process and follow up when necessary.

## Steps necessary to run the software

Start by setting up pipenv and its specified dependencies
```
pip install pipenv
pipenv install
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

See instructions. Delete this line and place a link to the task boards here.

## Team members

* Wilson Xu [Profile](https://github.com/wilsonxu101)
* Hanna Han [Profile](https://github.com/HannaHan2)
* Sewon Kim [Profile](https://github.com/SewonKim0)