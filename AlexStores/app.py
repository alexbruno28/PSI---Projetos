
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from auth.routes import auth_bp
from controllers.user_controller import user_bp
from controllers.product_controller import product_bp
import auth.utils  


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)
    login_manager.init_app(app)

   
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')

    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

   
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
