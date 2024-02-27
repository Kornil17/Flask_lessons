from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, as_declarative, declared_attr
from settings import Config
from loguru import logger
from datetime import datetime

logger.add('db.logs', format='{time} {level} {message}', level='DEBUG', encoding='UTF8')



data = Config.get_settings()
engine = create_engine(
    url=f"postgresql://{data['database']['username']}:{data['database']['password']}@{data['database']['host']}:{data['database']['port']}/{data['database']['db_name']}",
    echo=True
)

metadata = MetaData()
session = sessionmaker(engine)

@as_declarative()
class AbsractModel:
    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
class Menu(AbsractModel):
    __tablename__ = 'mainmenu'

    title: Mapped[str]
    url: Mapped[str]

    def __iter__(self):
        return self

class Users(AbsractModel):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    time: Mapped[datetime] = mapped_column(default=datetime.utcnow())

class Posts(AbsractModel):
    __tablename__ = 'posts'

    title: Mapped[str]
    text: Mapped[str]
    time: Mapped[datetime] = mapped_column(default=datetime.utcnow())



class WorkDb:
    @classmethod
    def get_menu(cls) -> list:
        try:
            with session() as conn:
                data = conn.query(Menu).all()
                return [dict(d.__dict__) for d in data]
        except Exception as error:
            logger.error(f"Got error by get menu -> {error}")
    @classmethod
    def insert_menu_data(cls, title, url) -> int:
        try:
            with session() as conn:
                menu = Menu(title=title, url=url)
                data = conn.add(menu)
                conn.commit()
                return menu.id
        except Exception as error:
            logger.error(f"Got error by indert menu -> {error}")

    @classmethod
    def add_post(cls, title, text) -> int:
        try:
            with session() as conn:
                post = Posts(title=title, text=text)
                data = conn.add(post)
                conn.commit()
                return True
        except Exception as error:
            logger.error(f"Got error by add post -> {error}")
            return False
    @classmethod
    def get_post(cls, id) -> list:
        try:
            with session() as conn:
                data = conn.query(Posts).filter_by(id=id).first()
                return data
        except Exception as error:
            logger.error(f"Got error by get post -> {error}")
    @classmethod
    def get_all_posts(cls) -> dict:
        try:
            with session() as conn:
                data = conn.query(Posts).all()
                return [dict(d.__dict__) for d in data]

        except Exception as error:
            logger.error(f"Got error by get all post -> {error}")

    @classmethod
    def addUser(cls, username, email, password) -> bool:
        try:
            with session() as conn:
                user = Users(name=username, email=email, password=password)
                get_user = conn.query(Users).filter_by(name=username).first()
                logger.info(f'Get username from DB -> {get_user}')
                if get_user:
                    logger.error(f'Пользователь с именем -> {username} уже существует')
                    return False
                data = conn.add(user)
                conn.commit()
                return True
        except Exception as error:
            logger.error(f"Got error by add user -> {error}")
            return False

    @classmethod
    def get_user_id(cls, user_id: int) -> dict:
        try:
            with session() as conn:
                get_user = conn.query(Users).filter_by(id=user_id).first().__dict__
                del get_user['_sa_instance_state']
                return get_user
        except Exception as error:
            logger.error(f"Got error by get user info -> {error}")
def main():
    # AbsractModel.metadata.drop_all(engine)
    menu = [
        {"name": "Авторизация", "url": "login"},
        {"name": "Добавить статью", "url": "addPost"},
        {"name": "Обратная связь", "url": "contact"}
    ]
    # Users.__table__.drop(engine)
    AbsractModel.metadata.create_all(engine)
    logger.info(WorkDb.get_menu())
    # logger.info(WorkDb.get_user_id(1))
    # for i in menu:
    #     logger.info(WorkDb.insert_menu_data(title=i['name'], url=i['url']))
    # logger.info(WorkDb.get_post(id=1))
    # logger.info(WorkDb.get_all_posts())


if __name__ == '__main__':
    main()



