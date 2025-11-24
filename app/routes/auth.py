
from flask import Blueprint, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_pydantic import validate
from ..models import db, User
from ..schemas import UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/register", methods=["POST"])
@validate()
def register(body: UserRegisterSchema):
    if User.query.filter_by(email=body.email).first():
        return jsonify({"error": "이미 존재하는 이메일입니다."}), 409

    hashed_password = generate_password_hash(body.password)
    new_user = User(name=body.name, email=body.email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "회원가입이 성공적으로 완료되었습니다.", "user_id": new_user.user_id}), 201

@auth_bp.route("/login", methods=["POST"])
@validate()
def login(body: UserLoginSchema):
    user = User.query.filter_by(email=body.email).first()
    if user and check_password_hash(user.password, body.password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "이메일 또는 비밀번호가 올바르지 않습니다."}), 401
