import pymongo
import config
from pymongo import MongoClient
from pymongo.collection import Collection


class DataBaseConnection:

    def __init__(self, connection_string: str, database: str) -> None:
        self._connection_string: str = connection_string
        self._client: MongoClient = MongoClient(connection_string)
        self._db = self._client[database]

        self._db['users'].create_index(
            [('login', pymongo.ASCENDING)],
            name='login_index'
        )
        self._db['languages'].create_index(
            [('code', pymongo.ASCENDING)],
            name='code_index'
        )

    def getCollection(self, name: str) -> Collection:
        return self._db[name]


db_connection = DataBaseConnection(
    config.connection_string,
    config.database_name
)

db_users: Collection = db_connection.getCollection("users")
db_translations: Collection = db_connection.getCollection("translations")
db_languages: Collection = db_connection.getCollection("languages")
