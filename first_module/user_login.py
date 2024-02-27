from dataclasses import dataclass
from database import WorkDb
class UserLogin():
    @classmethod
    def get_user(cls, user_id: int):
        cls.__user = WorkDb.get_user_id(user_id)

    @classmethod
    def create(cls, user):
        cls.__user = user
        return cls
    @classmethod
    def is_authenticated(cls) -> bool:
        return True

    @classmethod
    def is_active(cls) -> bool:
        return True

    @classmethod
    def is_anonymous(cls) -> bool:
        return False

    @classmethod
    def get_id(cls) -> str:
        return str(cls.__user['id'])

