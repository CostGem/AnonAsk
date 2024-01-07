from typing import Dict, List, Tuple

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner

FLUENT_DICTIONARIES_PATH_DICT = {
    "ru": "src/translation/locales/ru.ftl",
}

FLUENT_TRANSLATORS: List[FluentTranslator] = [
    FluentTranslator(
        locale=locale,
        translator=FluentBundle.from_files(
            locale=locale, filenames=[FLUENT_DICTIONARIES_PATH_DICT[locale]]
        ),
    )
    for locale in FLUENT_DICTIONARIES_PATH_DICT
]

FLUENT_LOCALES_MAP: Dict[str, Tuple[str]] = {
    "ru": ("ru",),
}


class LocalizedTranslator:
    translator: TranslatorRunner
    locale: str

    def __init__(self, translator: TranslatorRunner, locale: str):
        self.translator = translator
        self.locale = locale

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)


class TranslatorManager:
    t_hub: TranslatorHub
    translators: Dict[str, LocalizedTranslator] = {}

    def __new__(cls) -> "TranslatorManager":
        if not hasattr(cls, "instance"):
            cls.instance = super(TranslatorManager, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.t_hub = TranslatorHub(
            locales_map=FLUENT_LOCALES_MAP,
            translators=FLUENT_TRANSLATORS,
            root_locale="ru",
        )
        self.__init_translators()

    def __init_translators(self) -> None:
        """The function initializes translators for each locale using the t_hub object"""
        for locale in self.t_hub.locales_map:
            self.translators[locale] = LocalizedTranslator(
                translator=self.t_hub.get_translator_by_locale(locale), locale=locale
            )

    def get_translator(self, locale: str) -> LocalizedTranslator:
        if locale not in self.translators:
            locale = self.t_hub.root_locale

        return self.translators[locale]
