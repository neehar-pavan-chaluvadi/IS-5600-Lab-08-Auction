from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_admin import Admin
from admin import ProductViews

from flask_admin.contrib.sqla import ModelView
from config import Config
from extensions import db, jwt
from views import (
    RegisterUser,
    UserLogin,
    Person,
    ProductCatalogue,
    UpdateBidAmount,
)
from models import User, Product, ProductBuyer

def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)
    admin = Admin(app)
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(User, db.session))

    api.add_resource(RegisterUser, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(Person, '/users', '/user/<int:user_id>')
    api.add_resource(UpdateBidAmount, '/raise_bid')
    api.add_resource(ProductCatalogue, '/items')

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8089)
