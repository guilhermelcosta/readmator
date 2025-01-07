import requests

from util.constants import GOOGLE_TRANSLATE_API_URL, SOURCE_LANGUAGE, TARGET_LANGUAGE, TEXT


def translate_text(text, source_language, target_language):

    url = GOOGLE_TRANSLATE_API_URL.replace(TEXT, f"{text}") \
        .replace(SOURCE_LANGUAGE, source_language) \
        .replace(TARGET_LANGUAGE, target_language)

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()[0][0][0]
    return None
