from typing import Optional

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner

from config import LANG_CODE_LIST
from errors.translation import InvalidTranslationKeyError


class Translator:
    """Translator"""

    __translator_hub: TranslatorHub

    def __init__(self) -> None:
        self.__translator_hub = TranslatorHub(
            locales_map={
                "en": ("en", "ru"),
                "ru": ("ru", "en"),
            },
            translators=[
                FluentTranslator(
                    locale="ru",
                    translator=FluentBundle.from_files("ru-RU", filenames=["src/locales/locale_dicts/ru.ftl"])
                ),
                FluentTranslator(
                    locale="en",
                    translator=FluentBundle.from_files("en-US", filenames=["src/locales/locale_dicts/en.ftl"])
                ),
            ],
            root_locale="en"
        )

    def __call__(self, locale_code: str, *args, **kwargs):
        return LocalizedTranslator(
            translator=self.__translator_hub.get_translator_by_locale(locale=locale_code),
            locale=locale_code if locale_code in LANG_CODE_LIST else self.__translator_hub.root_locale
        )


class LocalizedTranslator:
    """LocalizedTranslator"""

    __translator: TranslatorRunner
    locale: str

    def __init__(self, locale: str, translator: TranslatorRunner) -> None:
        self.__translator = translator
        self.locale = locale

    def get(self, key: str, **kwargs) -> str:
        """
        Returns a value from a language dictionary by key
        :param key: Value key in the language dictionary
        :return: Meaning from the language dictionary
        """

        translation: Optional[str] = self.__translator.get(key, **kwargs)

        if not translation:
            raise InvalidTranslationKeyError(key=key)

        return translation
