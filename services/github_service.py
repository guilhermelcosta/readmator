from http import HTTPStatus

from services.request_service import perform_request
from services.translate_service import translate_text
from util.constants import GITHUB_TOKEN, GITHUB_README_URL, SOURCE_LANGUAGE, TARGET_LANGUAGE, INDEX_ZERO, TARGET_LANGUAGE_SEPARATOR
from util.parameters_util import extract_parameters


def update_readme_service():
    readme = _get_readme(GITHUB_TOKEN)
    source_language = extract_parameters(readme, SOURCE_LANGUAGE)
    target_language = extract_parameters(readme, TARGET_LANGUAGE)[INDEX_ZERO].split(TARGET_LANGUAGE_SEPARATOR)

    for language in target_language:
        translated_readme = translate_text(readme, source_language[INDEX_ZERO], language)


def _get_readme(github_token):
    headers = {
        "Authorization": f"Bearer {github_token}",
    }
    response = perform_request(GITHUB_README_URL, "GET", headers)
    # todo: logica deve ficar no request service
    if response.status_code != HTTPStatus.OK:
        return None
    return response.text
