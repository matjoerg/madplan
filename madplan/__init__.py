import os
from flask import Flask
from madplan.model import model
import webbrowser

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from .views import welcome
    app.register_blueprint(welcome.bp)

    model.init_app(app)

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open('http://localhost:5000')
    return app
