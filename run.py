from flask import Flask
from config import Config
from extensions import db

from routes.cliente import cliente_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(cliente_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

        # 🔐 cria admin padrão se não existir
        from models.user import User
        from werkzeug.security import generate_password_hash

        admin = User.query.filter_by(username="admin").first()

        if not admin:
            admin = User(
                username="admin",
                password=generate_password_hash("1234"),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)