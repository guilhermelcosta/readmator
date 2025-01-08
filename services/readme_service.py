import os
import re
from http import HTTPStatus

from dotenv import load_dotenv

from constants.constants import SOURCE_LANGUAGE, TARGET_LANGUAGE, INDEX_ZERO, TARGET_LANGUAGE_SEPARATOR, \
    INDEX_ONE, GITHUB_README_URL, GITHUB_TOKEN
from services.request_service import perform_request
from services.translate_service import translate_text
from util.formater_util import extract_readme_parameters, sanitize_segment

load_dotenv()


async def update_readme_service():
    readme_content = _fetch_readme(os.getenv(GITHUB_TOKEN))
    translated_segments = await _translate_segments(_parse_languages(readme_content), _extract_segments_to_translate(readme_content))

    return translated_segments


async def _translate_segments(languages, segments_to_translate):
    translated_segments = []

    for i in range(len(languages[INDEX_ONE])):
        language_array = []
        for j in range(len(segments_to_translate)):
            language_array.append(await translate_text(segments_to_translate[j], languages[INDEX_ZERO], languages[INDEX_ONE][i]))
        translated_segments.append(language_array)

    return translated_segments


def _fetch_readme(github_token):
    response = perform_request(os.getenv(GITHUB_README_URL), "GET", github_token)
    if not response or response.status_code != HTTPStatus.OK:
        raise RuntimeError("Failed to fetch the README from GitHub.")
    return response.text


def _extract_segments_to_translate(readme_content, tag_name="class", tag_value="translate"):
    translate_segments = re.findall(rf'<.*?{tag_name}=["\']{tag_value}["\'].*?>(.*?)</.*?>', readme_content, re.DOTALL)
    return [sanitize_segment(segment) for segment in translate_segments]


def _parse_languages(readme_content):
    source_language = extract_readme_parameters(readme_content, SOURCE_LANGUAGE)
    target_languages = extract_readme_parameters(readme_content, TARGET_LANGUAGE)[INDEX_ZERO].split(TARGET_LANGUAGE_SEPARATOR)
    return source_language[INDEX_ZERO].lower(), [language.lower() for language in target_languages]
