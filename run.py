from src.app import create_app
from src.app import get_db
app = create_app()
if __name__ == '__main__':
    with app.app_context():
        app.run(port='5000', debug=True)