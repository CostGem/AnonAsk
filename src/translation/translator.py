import os
from typing import Dict, List, TypeVar

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner

from src.enums.service.locale import LocalesEnum

TranslatorGeneric = TypeVar("TranslatorGeneric", bound="TranslatorManager")

FLUENT_DICTIONARIES_PATH_DICT: Dict[str, str] = {
    LocalesEnum.RU: "src/translation/locales/ru/",
}

FLUENT_TRANSLATORS: List[FluentTranslator] = [
    FluentTranslator(
        locale=locale,
        translator=FluentBundle.from_files(
            use_isolating=False,
            locale=locale,
            filenames=[
                FLUENT_DICTIONARIES_PATH_DICT[locale] + dictionary_file
                for dictionary_file in os.listdir(path=FLUENT_DICTIONARIES_PATH_DICT[locale])
            ]
        ),
    )
    for locale in FLUENT_DICTIONARIES_PATH_DICT
]

FLUENT_LOCALES_MAP: Dict = {
    LocalesEnum.RU: (LocalesEnum.RU,),
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

    def __new__(cls) -> TranslatorGeneric:
        if not hasattr(cls, "instance"):
            cls.instance = super(TranslatorManager, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        if not hasattr(self, "t_hub"):
            self.t_hub = TranslatorHub(
                locales_map=FLUENT_LOCALES_MAP,
                translators=FLUENT_TRANSLATORS,
                root_locale=LocalesEnum.RU,
            )
            self.__init_translators()

    def __init_translators(self) -> None:
        """The function initializes translators for each locale using the t_hub object"""

        for locale in self.t_hub.locales_map:
            self.translators[locale] = LocalizedTranslator(
                translator=self.t_hub.get_translator_by_locale(locale), locale=locale
            )

    def get_translator(self, locale: LocalesEnum) -> LocalizedTranslator:
        """
        Returns a translator from translators list

        :param locale: Locale code
        """

        if locale not in self.translators:
            locale = self.t_hub.root_locale

        return self.translators[locale]
