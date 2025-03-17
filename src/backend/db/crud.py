from db import db, models
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, query

def get_db_session() -> scoped_session:
    """ 新しいDBコネクションを返す
    """
    return scoped_session(sessionmaker(db.engine))

class BaseCRUD:
    def __init__(self, db_session: scoped_session, model: db.Base):
        self.db_session = db_session
        self.model = model

    def get_query(self):
        return self.model.query

    def gets(self):
        """ 全件取得
        """
        return self.db_session.query(self.model).all()

    def get_by_id(self, id: int):
        """ 主キーで取得
        """
        return self.get_query().filter_by(id=id).first()

    def create(self, data: dict = {}):
        """ 新規登録
        """
        obj = self.model()
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.add(obj)
        self.db_session.flush()
        self.db_session.refresh(obj)
        self.db_session.commit()
        return obj

    def update(self, obj, data: dict = {}):
        """ 更新
        """
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.flush()
        self.db_session.refresh(obj)
        self.db_session.commit()
        return obj

    def delete_by_id(self, id: int):
        """ 主キーで削除
        """
        obj = self.get_by_id(id)
        if obj:
            obj.delete()
            self.db_session.flush()
        return None

    def delete(self, **kwargs):
        """ 主キーで削除
        """
        self.db_session.filter_by(**kwargs).delete()
        self.db_session.flush()
        self.db_session.commit()
        return None

    def create_column(self, data: dict = {}):
        column = sqlalchemy.Column(data['column_code'], sqlalchemy.String(255))
        print(column)
        self.db_session.execute('ALTER TABLE %s ADD COLUMN %s %s' % (self.model.__tablename__, column.name, column.type))
        self.db_session.commit()

    def delete_column(self, data: dict = {}):
        column = sqlalchemy.Column(data['column_code'], sqlalchemy.String(255))
        print(column)
        self.db_session.execute('ALTER TABLE %s ADD COLUMN %s %s' % (self.model.__tablename__, column.name, column.type))
        self.db_session.commit()