from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db
from routes.products import product_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(product_bp, url_prefix='/api/products')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
