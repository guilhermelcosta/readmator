from flask import Blueprint, jsonify

from services.readme_service import update_readme_service

readme_blueprint = Blueprint("github", __name__)


@readme_blueprint.route('/')
async def update_readme():
    return jsonify(await update_readme_service()), 200
