import re
from datetime import datetime

from sqlalchemy.orm import query, Mapped, mapped_column, as_declarative, sessionmaker, relationship
from sqlalchemy import MetaData,engine, create_engine, ForeignKey, or_

from settings import Config

data = Config.get_settings()
engine = create_engine(
    url=f"postgresql://{data['database']['username']}:{data['database']['password']}@{data['database']['host']}:{data['database']['port']}/{data['database']['db_name']}",
    echo=False
)
metadata = MetaData()
session = sessionmaker(engine)
@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(primary_key=True)

class Post(AbstractModel):
    __tablename__ = 'blog_posts'

    title: Mapped[str]
    body: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

class Tag(AbstractModel):
    __tablename__ = 'tags'

    name: Mapped[str]

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)

class PostTag(AbstractModel):
    __tablename__ = 'post_tags'

    post_id: Mapped[int] = mapped_column(ForeignKey(Post.id))
    tag_id: Mapped[int] = mapped_column(ForeignKey(Tag.id))


class DataManager:
    @classmethod
    def insert_data(cls, cl_name, **kwargs) -> None:
        try:
            with (session() as conn):
                result = cl_name(**kwargs)
                conn.add(result)
                conn.commit()
                print(result.id)

        except Exception as error:
            print(error)
    @classmethod
    def get_post_by_id(cls, id) -> list:
        try:
            with (session() as conn):
                get_id = conn.query(Post).filter_by(id=id).scalar()
            return get_id
        except Exception as error:
            print(error)
    @classmethod
    def get_all_posts(cls, name=None) -> list:
        try:
            with (session() as conn):
                if name:
                    posts = conn.query(Post).filter(or_(Post.title.contains(name.lower().strip()), Post.body.contains(name.lower().strip()))).all()
                    return [dict(p.__dict__) for p in posts]
                posts = conn.query(Post).all()
            return [dict(p.__dict__) for p in posts]

        except Exception as error:
            print(error)
    @classmethod
    def get_tag_by_id(cls, id) -> list:
        try:
            with (session() as conn):
                get_id = conn.query(Tag).filter_by(id=id).scalar()
            return get_id
        except Exception as error:
            print(error)

def main():
    AbstractModel.metadata.create_all(engine)
    # DataManager.insert_data('test', 'body')
    data = [
        {"title":"Python", "body":"simple language"},
        {"title": "C", "body": "base language"},
        {"title": "C++", "body": "base language after C"},
        {"title": "GO", "body": "new language"},
        {"title": "Java", "body": "popular language"}
    ]
    data2 = [
        {"name":"simple"},
        {"name": "hard"},
        {"name": "middle"}
    ]
    data3 = [
        {"post_id":"2", "tag_id":"1"},
        {"post_id": "3", "tag_id": "3"},
        {"post_id": "4", "tag_id": "3"},
        {"post_id": "5", "tag_id": "2"},
        {"post_id": "6", "tag_id": "2"}
    ]
    # for d in data3:
    #     DataManager.insert_data(PostTag, **d)
    # print(DataManager.get_post_by_id(1))
    print(DataManager.get_all_posts())


if __name__ == "__main__":
    main()
