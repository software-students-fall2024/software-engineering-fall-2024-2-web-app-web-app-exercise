# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

This Project Tracker App is an intelligent task management tool that divides tasks, assigns them based on team skill sets and workload, tracks progress visually, and provides personalized to-do lists for clear accountability and efficient project completion.

## User stories
[Issues Link for User Stories](https://github.com/software-students-fall2024/2-web-app-n-a-j/issues)

1. As a `team member`, I want to view the projects I am part of so that I can see the tasks assigned to me.

2. As an `event organizer`, I want to create new projects so that I can organize and track the tasks my team needs to complete.

3. As a `user`, I want to view my profile so that I can see my personal name and workspaces.

4. As a `team member`, I want to be able to view what other tasks within the project my team members have, so that I can better collaborate with my teammates.

5. As a `user`, I want to log out of the system so that I can secure my account when I'm done using it.

6. As a `manager`, I want to edit project details and task assignment so that I can keep the information up-to-date as things change.

7. As a `user`, I want to search for specific tasks so that I can quickly find the information I need.

## Steps Necessary to Run the Software

To run the software, follow these steps:

1. **Install Python**:
   - Make sure Python 3.8 or higher is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Clone the repository**:
   - Download the project by cloning the GitHub repository or downloading the project files manually:
     ```bash
     git clone https://github.com/software-students-fall2024/2-web-app-n-a-j
     cd your-repository-folder
     ```

3. **Set up a virtual environment**:
   - Run the following commands to create and activate the virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       .\venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install dependencies**:
   - Use the `requirements.txt` file to install the necessary Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

5. **Set up environment variables**:
   - Create a `.env` file in the root directory of your project and add the following variables:
     ```env
     MONGO_DBNAME=tasks
     MONGO_URI=mongodb+srv://FriedBananaBan:Wc6466512288@project2.nzxyf.mongodb.net/?retryWrites=true&w=majority&appName=project2
     FLASK_APP=app.py
     FLASK_ENV=development
     FLASK_PORT=3000
     ```

6. **Run the application**:
   - In the terminal (while your virtual environment is activated), run:
     ```bash
     python app.py
     ```

7. **Access the application**:
   - Open a web browser and go to `http://127.0.0.1:3000/` to access the application interface.

8. **Deactivating the virtual environment**:
   - When finished, deactivate the virtual environment by typing:
     ```bash
     deactivate
     ```

## Task boards

- **Sprint 1** [Task Boards](https://github.com/orgs/software-students-fall2024/projects/30)
- **Sprint 2** [Task Boards](https://github.com/orgs/software-students-fall2024/projects/49)

## Team members

- **Jessica Xu** (kx2053) [GitHub Profile](https://github.com/Jessicakk0711)
- **Terry Cao** (tc3661) [GitHub Profile](https://github.com/cao-exe)
- **William Cao** (wc2723) [GitHub Profile](https://github.com/FriedBananaBan)
- **Boming Zhang** (bz2196) [GitHub Profile](https://github.com/BomingZhang-coder)
- **Hang Yin** (hy2270) [GitHub Profile](https://github.com/Popilopi168)
