# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     CORS(app)
#     app.config.from_object('config.Config')

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # with app.app_context():
#     #     from . import routes
#     #     db.create_all()  # Isso será gerenciado pelas migrações após a inicialização inicial

#     return app


from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "PUT"], "allow_headers": ["Content-Type", "X-Requested-With","Authorization", "application/json"]}})
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Aplica CORS a todas as rotas
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    

    return app
