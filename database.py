from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, as_declarative, declared_attr
from settings import Config

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




if __name__ == '__main__':
    Menu()




