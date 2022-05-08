import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    privilege_level = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    form_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("forms.id"))
    form = orm.relation('Form')