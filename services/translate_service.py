from googletrans import Translator

translator_instance = Translator()


async def translate_text(text, source_language, target_language):
    result = await translator_instance.translate(
        text,
        src=source_language,
        dest=target_language
    )
    return result.text
