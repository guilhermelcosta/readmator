# from flask import Blueprint, request, jsonify
# from services.translate_service import translate_text
#
# translate_blueprint = Blueprint("translate", __name__)
#
#
# @translate_blueprint.route('/', methods=['POST'])
# def translate_text():
#     data = request.get_json()
#     if not data or "text" not in data:
#         return {"error": "Text to translate is missing"}, 400
#
#     translation = translate_text(data["text"])
#     if translation:
#         return jsonify({"translation": translation}), 200
#     return {"error": "Translation failed"}, 500
