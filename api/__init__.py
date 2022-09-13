from flask import Flask, jsonify
from .helpers import set_flask_environment
from .extensions import mail, db, ma, cors, swagger
from .mail_blueprint.views import mail as mail_blueprint
from flasgger import LazyJSONEncoder


def create_app(scrpt_info=None):
    """Create the flask application."""
    
    app = Flask(__name__)
    
    set_flask_environment(app)
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Check if the application is running."""
        return jsonify({'Hello': 'From mail service'}), 200
    
    # initialize extensions
    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    app.json_encoder = LazyJSONEncoder
    swagger.init_app(app)
    
    app.register_blueprint(mail_blueprint, url_prefix='/api/v1/mail')
    
    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app