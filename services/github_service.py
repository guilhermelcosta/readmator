import re
from http import HTTPStatus

from services.request_service import perform_request
from services.translate_service import translate_text
from util.constants import GITHUB_TOKEN, GITHUB_README_URL, SOURCE_LANGUAGE, TARGET_LANGUAGE, INDEX_ZERO, TARGET_LANGUAGE_SEPARATOR
from util.parameters_util import extract_parameters


async def update_readme_service():
    readme = _get_readme(GITHUB_TOKEN)
    matches = re.findall(r'<.*?class=["\']translate["\'].*?>(.*?)<\/.*?>', readme, re.DOTALL)
    source_language = extract_parameters(readme, SOURCE_LANGUAGE)
    target_language = extract_parameters(readme, TARGET_LANGUAGE)[INDEX_ZERO].split(TARGET_LANGUAGE_SEPARATOR)
    result = []

    for i in range(len(matches)):
        for j in range(len(target_language)):
            result.append(await translate_text(matches[i].replace('\n', ' ').replace('\r', ''),
                                               source_language[INDEX_ZERO].lower(),
                                               target_language[j].lower()))

    return result, 200


def _get_readme(github_token):
    headers = {
        "Authorization": f"Bearer {github_token}",
    }
    response = perform_request(GITHUB_README_URL, "GET", headers)
    if response.status_code != HTTPStatus.OK:
        return None
    return response.text
