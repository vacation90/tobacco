import collections
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from db import session
from sqlalchemy.sql import func
# import session
from sqlalchemy.orm import relationship

class Users(session.Base):
    __tablename__ = 'users'
    email = sqlalchemy.Column(sqlalchemy.TEXT, unique=True, nullable=False, primary_key=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.VARCHAR(128), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False, default=True)

class Columns(session.Base):
    __tablename__ = 'columns'
    code = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), unique=True)
    list_value = relationship('ListValues', backref='listvalues', lazy='joined')
    unit = sqlalchemy.Column(sqlalchemy.String(255))
    data_type = sqlalchemy.Column(sqlalchemy.String(255))
    @hybrid_method
    def sql_data_type(self):
        print('method sql_data_type: ', self.data_type)
        if self.data_type == 'int':
            return sqlalchemy.Integer()
        elif self.data_type == 'num':
            return sqlalchemy.Numeric()
        elif self.data_type == 'date':
            return sqlalchemy.Date()
        else:
            return sqlalchemy.String()


class ListValues(session.Base):
    __tablename__ = 'listvalues'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    column = sqlalchemy.Column(sqlalchemy.String(255), sqlalchemy.ForeignKey('columns.code', onupdate='CASCADE', ondelete='CASCADE'))
    name = sqlalchemy.Column(sqlalchemy.String(255), unique=True)

class MainItems(session.Base):
    __tablename__ = 'mainitems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)


if session.engine.has_table('columns'):
    db_session = session.SessionLocal()
    for column in db_session.query(Columns).all():
        print(column.code, column.name, column.data_type)
        if column.data_type:
            # print(type(Columns.sql_data_type))
            setattr(MainItems, column.code, sqlalchemy.Column(Columns.sql_data_type()))
    db_session.close()
