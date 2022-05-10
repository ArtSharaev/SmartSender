"""status: 0 - на модерации, 1 - отклонена, 2 - верифицирована"""


import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Form(SqlAlchemyBase):
    __tablename__ = 'forms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    from_tg_user_id = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    moderator_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    changed_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user = orm.relation("User", back_populates='form')