
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from ..models import db, User, Project
from ..schemas import ProjectCreateSchema, ProjectUpdateSchema

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')
portfolio_projects_bp = Blueprint('portfolio_projects', __name__, url_prefix='/portfolio')

@portfolio_projects_bp.route("/<int:user_id>/projects", methods=["POST"])
@jwt_required()
@validate()
def add_project_to_portfolio(user_id, body: ProjectCreateSchema):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "자신의 포트폴리오에만 프로젝트를 추가할 수 있습니다."}), 403

    User.query.get_or_404(user_id)
    new_project = Project(user_id=user_id, **body.model_dump())

    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "프로젝트가 성공적으로 추가되었습니다.", "project": new_project.to_dict()}), 201

@projects_bp.route("/<string:project_id>", methods=["PUT"])
@jwt_required()
@validate()
def update_project(project_id, body: ProjectUpdateSchema):
    project = Project.query.get_or_404(project_id)
    if project.user_id != get_jwt_identity():
        return jsonify({"error": "권한이 없습니다."}), 403

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.session.commit()
    return jsonify({"message": "프로젝트가 성공적으로 수정되었습니다.", "project": project.to_dict()}), 200

@projects_bp.route("/<string:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != get_jwt_identity():
        return jsonify({"error": "권한이 없습니다."}), 403

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "프로젝트가 성공적으로 삭제되었습니다."}), 200
