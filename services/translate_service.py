from googletrans import Translator

from util.formater_util import capitalize_first_letter

translator_instance = Translator()


async def translate_text(text, source_language, target_language):
    result = await translator_instance.translate(
        text,
        src=source_language,
        dest=target_language
    )
    return capitalize_first_letter(result.text)
