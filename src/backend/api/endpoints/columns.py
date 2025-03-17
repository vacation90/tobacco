import os
from statistics import mode
from fastapi import APIRouter, Request, Body, Depends
from db import session, models
from api.endpoints import auth
from pydantic import BaseModel
from typing import List, Dict
from typing import Optional
import sqlalchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.operations import Operations

alembic_cfg = Config('alembic.ini')
router = APIRouter()

# ListValueの返り値定義
class ListValuesResponse(BaseModel):
    name: str
    class Config():
        orm_mode = True

# 全Columnを返すエンドポインt
@router.get('/all')
def get_items(db_session: Session=Depends(session.get)):
    int_columns = []
    # 全Column取得
    columns_all = db_session.query(
        models.Columns,
    ).all()
    # 各Columnの処理
    return_columns = []
    for column in columns_all:
        # 返す基本データの作成
        return_column = {
            'code': column.code,
            'name': column.name,
            'list_value': column.list_value,
            'unit': column.unit,
            'data_type': column.data_type,
        }
        # 数値型の処理
        # フロントエンドでのフィルタの最大値最小値の追加
        if column.data_type == 'int' or column.data_type == 'num':
            return_column['value_range'] = [
                db_session.query(func.min(getattr(models.MainItems, column.code))).one()[0],
                db_session.query(func.max(getattr(models.MainItems, column.code))).one()[0],
            ]
        # 日付型の処理
        # フロントエンドでのフィルタの最大最小日時の追加
        elif column.data_type == 'date':
            return_column['date_range'] = {
                'start': db_session.query(func.min(getattr(models.MainItems, column.code))).one()[0],
                'end': db_session.query(func.max(getattr(models.MainItems, column.code))).one()[0],
            }
        return_columns.append(return_column)
    return return_columns

# Columnの追加用POSTパラメータ定義
class AddColumnParam(BaseModel):
    code: str
    name: str
    default_value: str
    data_type: str

# Column追加用エンドポイント
@router.post('/add')
async def add(
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    add_column_params: List[AddColumnParam] = Body(
        ...,
        example = [
            {"code": "maker", "name": "メーカー", "data_type": "String", "default_value": "日本たばこ産業株式会社",},
        ]
    )
):
    # 各レコードの処理
    for add_column_param in add_column_params:
        # 同じColumnCodeが存在しない場合のみ追加
        if not db_session.query(models.Columns).filter_by(code = add_column_param.dict()['code']).scalar():
            # カラム定義取得
            add_column = models.Columns()
            # 各パラメータからカラム定義を呼び出す
            for key, value in add_column_param.dict().items():
                # パラメータが絡む定義に一致したら追加
                if hasattr(add_column, key):
                    setattr(add_column, key, value)
            db_session.add(add_column)
            db_session.commit()

            setattr(models.MainItems, add_column_param.dict()['code'], sqlalchemy.Column(getattr(sqlalchemy, 'String')))

# Columnの更新用POSTパラメータ定義
class UpdateColumnParam(BaseModel):
    code: str
    name: str
    default_value: str
    data_type: str

# Column更新用エンドポイント
@router.post('/update')
async def update(
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    update_column_params: List[UpdateColumnParam] = Body(
        ...,
        example=[
            {"code": "maker", "name": "メーカー", "data_type": "String", "default_value": "日本たばこ産業株式会社",},
            {"code": "name", "name": "Title", "data_type": "Integer", "default_value": "", "unit": "mg"}
        ]
    )
):
    # 各レコードの処理
    for update_column_param in update_column_params:
        update_column_param_dict = update_column_param.dict()
        # 更新対象のカラム取得
        update_column = db_session.query(models.Columns).filter(models.Columns.code == update_column_param_dict['code']).all()[0]
        # 各パラメータからカラム定義を呼び出す
        for key, value in update_column_param_dict.items():
            # パラメータが絡む定義に一致したら追加
            if key != 'code' and hasattr(update_column, key):
                setattr(update_column, key, value)

    try:
        # コミット
        db_session.commit()
    except:
        # 更新失敗したらロールバック
        db_session.rollback()
        return False
    return True


# Columnの削除用POSTパラメータ定義
class DeleteColumnParam(BaseModel):
    code: str

# Column削除用エンドポイント
@router.post('/delete')
async def delete(
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    delete_column_params: List[DeleteColumnParam] = Body(
        ...,
        example=[{"code": "name"}]
    )
):
    # 各レコードの処理
    for delete_column_param in delete_column_params:
        delete_column_param_dict = delete_column_param.dict()
        # 各パラメータからカラム定義を呼び出す
        db_session.query(models.Columns).filter(models.Columns.code == delete_column_param_dict['code']).all()[0].delete()

    try:
        # コミット
        db_session.commit()
    except:
        # 更新失敗したらロールバック
        db_session.rollback()
        return False
    return True
