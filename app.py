import os
from flask import Flask, render_template, request, redirect, url_for

def create_app():
    """
    Create and configure the Flask application.
    returns: app: the Flask application object
    """

    app = Flask(__name__)

    @app.route("/")
    def home_screen():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
                
        return render_template("home.html")
    
    @app.route("/start-session")
    def session_form():
        """
        Route for the home page.
        Returns:
            rendered template (str): The rendered HTML template.
        """
        return render_template("start-session.html")
    
    @app.route("/start-session", methods=["POST"])
    def create_session():
        """
        Route for POST requests to the create page.
        Accepts the form submission data for a new document and saves the document to the database.
        Returns:
            redirect (Response): A redirect response to the home page.
        """
        focus_time = request.form['focus']
        break_time = request.form['break']
        reps_no = request.form['reps']
        # add session info to database
        return redirect(url_for("counter"))
    
    @app.route("/congrats")
    def congrats():
        """
        Route for the congratulations page.
        Renders a template that shows the session details and a congratulations message.
        """
        focus_time = request.args.get('focus')
        break_time = request.args.get('break_time')
        reps_no = request.args.get('reps')
        
        return render_template("congrats.html", focus_time=focus_time, break_time=break_time, reps_no=reps_no)

    return app

    return app

if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)