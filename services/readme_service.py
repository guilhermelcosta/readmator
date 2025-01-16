import os
import re
from http import HTTPStatus

from dotenv import load_dotenv

from constants.constants import SOURCE_LANGUAGE, TARGET_LANGUAGE, INDEX_ZERO, TARGET_LANGUAGE_SEPARATOR, \
    INDEX_ONE, GITHUB_README_URL, GITHUB_TOKEN, STANDARD_TAG_NAME, STANDARD_TAG_VALUE
from services.github_service import create_files
from services.request_service import perform_request
from services.translate_service import translate_text
from util.formater_util import extract_readme_parameters, sanitize_segment

load_dotenv()

github_token = os.getenv(GITHUB_TOKEN)


async def update_readme_service():
    readme_content = _fetch_readme()
    translated_segments = await _translate_segments(_parse_languages(readme_content), _extract_segments_to_translate(readme_content))
    translated_readmes = _replace_translated_segments(readme_content, translated_segments)

    for i in enumerate(translated_readmes):
        create_files(f'minha-nova-pasta/arquivo-{i}.txt', os.getenv(GITHUB_TOKEN))

    return translated_readmes


async def _translate_segments(languages, segments_to_translate):
    translated_segments = []

    for i in range(len(languages[INDEX_ONE])):
        language_array = []
        for j in range(len(segments_to_translate)):
            language_array.append(await translate_text(segments_to_translate[j], languages[INDEX_ZERO], languages[INDEX_ONE][i]))
        translated_segments.append(language_array)

    return translated_segments


def _replace_translated_segments(readme_content, translated_segments, tag_name=STANDARD_TAG_NAME, tag_value=STANDARD_TAG_VALUE):
    matches = re.finditer(rf'<([a-zA-Z]+)[^>]*\b{tag_name}=["\']{tag_value}["\'][^>]*>(.*?)</.*?>', readme_content, re.DOTALL)
    match_list = [match.group() for match in matches]
    translated_segments_with_html = replace_translated_segment_inside_html(match_list, translated_segments)
    translated_readmes = replace_translated_segments_inside_readme(match_list, readme_content, translated_segments,
                                                                   translated_segments_with_html)
    return translated_readmes


def replace_translated_segments_inside_readme(match_list, readme_content, translated_segments, translated_segments_with_html):
    translated_readmes = []

    for i, translated_segment in enumerate(translated_segments):
        translated_readme = readme_content
        for j, match in enumerate(match_list):
            translated_readme = re.sub(match, translated_segments_with_html[i][j], translated_readme)
        translated_readmes.append(translated_readme)

    return translated_readmes


def replace_translated_segment_inside_html(match_list, translated_segments):
    translated_segments_with_html = []

    for i, translated_segment in enumerate(translated_segments):
        translated_segment_array = []
        for j, match in enumerate(match_list):
            translated_segment_array.append(re.sub(r'(>)([^<>]*)(<)', rf'\1{translated_segments[i][j]}\3', match))
        translated_segments_with_html.append(translated_segment_array)
    return translated_segments_with_html


def _fetch_readme():
    response = perform_request(os.getenv(GITHUB_README_URL), "GET", github_token)
    # todo: implement better treatment
    if not response or response.status_code != HTTPStatus.OK:
        raise RuntimeError("Failed to fetch the README from GitHub.")
    return response.text


def _extract_segments_to_translate(readme_content, tag_name=STANDARD_TAG_NAME, tag_value=STANDARD_TAG_VALUE):
    translate_segments = re.findall(rf'<.*?{tag_name}=["\']{tag_value}["\'].*?>(.*?)</.*?>', readme_content, re.DOTALL)
    return [sanitize_segment(segment) for segment in translate_segments]


def _parse_languages(readme_content):
    source_language = extract_readme_parameters(readme_content, SOURCE_LANGUAGE)
    target_languages = extract_readme_parameters(readme_content, TARGET_LANGUAGE)[INDEX_ZERO].split(TARGET_LANGUAGE_SEPARATOR)
    return source_language[INDEX_ZERO].lower(), [language.lower() for language in target_languages]
