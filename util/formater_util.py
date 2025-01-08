import re

from constants.constants import SPACE_CHARACTER, EMPTY_STRING, INDEX_ZERO, INDEX_ONE


def extract_readme_parameters(readme_content, parameter):
    return re.findall(rf'(?<={parameter}=")([^"]+)(?=")', readme_content)


def sanitize_segment(text):
    return (text
            .replace('\n', SPACE_CHARACTER)
            .replace('\r', EMPTY_STRING))


def capitalize_first_letter(text):
    return text[INDEX_ZERO].upper() + text[INDEX_ONE:] if text else EMPTY_STRING
