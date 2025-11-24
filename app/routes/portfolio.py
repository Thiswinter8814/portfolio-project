
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from sqlalchemy.orm.attributes import flag_modified
from ..models import db, User
from ..schemas import PortfolioUpdateSchema, SkillSchema

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route("/<int:user_id>", methods=["GET"])
def get_portfolio(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@portfolio_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@validate()
def update_portfolio(user_id, body: PortfolioUpdateSchema):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "자신의 포트폴리오만 수정할 수 있습니다."}), 403

    user = User.query.get_or_404(user_id)
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.session.commit()
    return jsonify({"message": "포트폴리오가 성공적으로 수정되었습니다.", "portfolio": user.to_dict()}), 200

@portfolio_bp.route("/skills", methods=["POST"])
@jwt_required()
@validate()
def add_skill(body: SkillSchema):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)

    new_skill = body.skill
    if new_skill in user.skills:
        return jsonify({"error": f"'{new_skill}'은(는) 이미 존재하는 기술 스택입니다."}), 409

    user.skills.append(new_skill)
    flag_modified(user, "skills")
    db.session.commit()
    return jsonify({"message": "기술 스택이 성공적으로 추가되었습니다.", "current_skills": user.skills}), 201

@portfolio_bp.route("/skills", methods=["DELETE"])
@jwt_required()
@validate()
def remove_skill(body: SkillSchema):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)

    skill_to_remove = body.skill
    if skill_to_remove not in user.skills:
        return jsonify({"error": f"'{skill_to_remove}'을(를) 찾을 수 없습니다."}), 404

    user.skills.remove(skill_to_remove)
    flag_modified(user, "skills")
    db.session.commit()
    return jsonify({"message": "기술 스택이 성공적으로 삭제되었습니다.", "current_skills": user.skills}), 200
