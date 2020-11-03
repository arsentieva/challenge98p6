from flask import Flask
from flask_migrate import Migrate
from app.config import Configuration
from app.models import db
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin


from app.routes.games import api as game
from app.routes.moves import api as move

app = Flask(__name__)
CORS(app)

app.config.from_object(Configuration)
db.init_app(app)
jwt = JWTManager(app)


api = Api(app)
api.add_namespace(game)
api.add_namespace(move)

migrate = Migrate(app, db)