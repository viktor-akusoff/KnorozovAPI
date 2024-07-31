from typing import Dict, Any
from pymongo.cursor import Cursor


class BaseSerializer:

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {}

    @classmethod
    def list_serialize(cls, obj_list: Cursor):
        return [cls.serialize(obj) for obj in obj_list]


class UserSerializer(BaseSerializer):

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {
            "id": str(obj["_id"]),
            "login": obj["login"],
            "password_hash": obj["password_hash"],
            "roles": obj["roles"]
        } if obj else None


class SafeUserSerializer(BaseSerializer):

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {
            "id": str(obj["_id"]),
            "login": obj["login"],
            "roles": obj["roles"]
        } if obj else None


class LanguageSerializer(BaseSerializer):

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {
            "id": str(obj["_id"]),
            "code": obj["code"],
            "name": obj["name"]
        } if obj else None


class TranslationPageSerializer(BaseSerializer):

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {
            "id": str(obj["_id"]),
            "name": obj["name"],
            "entries": obj["entries"]
        } if obj else None


class TranslationEntrySerializer(BaseSerializer):

    @staticmethod
    def serialize(obj) -> Dict[str, Any] | None:
        return {
            "key": obj["key"],
            "translations": obj["translations"]
        } if obj else None
