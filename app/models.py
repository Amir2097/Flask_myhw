from typing import Type
import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy as sq
from sqlalchemy_utils import EmailType, UUIDType

load_dotenv()
Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)


class Ads(Base):

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


class Token(Base):

    __tablename__ = "tokens"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


# def create_tables(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)


DSN = f'postgresql+psycopg2://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}' \
      f'@{os.getenv("HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
engine = sq.create_engine(DSN)
# create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

ORM_MODEL_CLS = Type[User] | Type[Ads] | Type[Token]
ORM_MODEL = User | Ads | Token
