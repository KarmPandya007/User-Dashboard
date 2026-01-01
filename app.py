import os
from flask import Flask
from flask_login import LoginManager
from routes import users_bp
from models import Person
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development-only')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login_page'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return Person.get_by_id(user_id)

app.register_blueprint(users_bp)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)