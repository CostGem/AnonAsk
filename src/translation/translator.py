import os
from typing import Dict, List, Tuple, TypeVar

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner

TranslatorGeneric = TypeVar("TranslatorGeneric", bound="TranslatorManager")

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

    def __new__(cls) -> TranslatorGeneric:
        if not hasattr(cls, "instance"):
            cls.instance = super(TranslatorManager, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.t_hub = TranslatorHub(
            locales_map=FLUENT_LOCALES_MAP,
            translators=self.get_fluent_translators_from_directory(locales_directory="src/translation/locales/"),
            root_locale="ru",
        )
        self.__init_translators()

    def get_fluent_translators_from_directory(self, locales_directory: str) -> List[FluentTranslator]:
        """
        Returns a fluent translators from a directory

        :param locales_directory: The directory with fluent files
        """

        translators: List[FluentTranslator] = []

        for locale_directory in os.listdir(path=locales_directory):
            if os.path.isdir(locale_directory):
                translators.append(
                    FluentTranslator(
                        locale=locales_directory,
                        translator=FluentBundle.from_files(
                            locale=locale_directory,
                            filenames=os.listdir(locale_directory)
                        ),
                    )
                )

        return translators

    def __init_translators(self) -> None:
        """The function initializes translators for each locale using the t_hub object"""

        for locale in self.t_hub.locales_map:
            self.translators[locale] = LocalizedTranslator(
                translator=self.t_hub.get_translator_by_locale(locale),
                locale=locale
            )

    def get_translator(self, locale: str) -> LocalizedTranslator:
        """Returns a translator from translators list"""

        if locale not in self.translators:
            locale = self.t_hub.root_locale

        return self.translators[locale]
