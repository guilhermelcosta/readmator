from flask import Blueprint, jsonify

from services.github_service import update_readme_service

github_blueprint = Blueprint("github", __name__)


@github_blueprint.route('/readme')
async def update_readme():
    response = await update_readme_service()
    if response:
        return jsonify(response), 200
    return {"error": "Failed to fetch README"}, 500
