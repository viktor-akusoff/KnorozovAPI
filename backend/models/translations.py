from pydantic import BaseModel
from typing import List


class TranslationEntry(BaseModel):
    key: str


class Translation(BaseModel):
    text: str


class TranslationPage(BaseModel):
    name: str
    entries: List[TranslationEntry] = []


class Language(BaseModel):
    code: str
    name: str


class LanguageUpdate(BaseModel):
    name: str
