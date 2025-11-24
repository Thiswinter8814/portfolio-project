
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, InternalServerError, Forbidden
from config import config
from .models import db
from .routes.auth import auth_bp
from .routes.portfolio import portfolio_bp
from .routes.projects import projects_bp, portfolio_projects_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(portfolio_projects_bp)

    @app.errorhandler(NotFound)
    def handle_not_found(e):
        description = getattr(e, 'description', "요청하신 리소스를 찾을 수 없습니다.")
        return jsonify(error=description), 404

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(e):
        return jsonify(error="서버에 예상치 못한 오류가 발생했습니다. 관리자에게 문의해주세요."), 500

    @app.errorhandler(Forbidden)
    def handle_forbidden(e):
        description = getattr(e, 'description', "접근 권한이 없습니다.")
        return jsonify(error=description), 403

    return app
