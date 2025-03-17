from fastapi import APIRouter, Request, Body, Depends
from db import session, models, crud
from api.endpoints import auth
import sqlalchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from pydantic import BaseModel
from typing import List
from typing import Optional

router = APIRouter()

@router.get('/all')
def get_columndict(db_session: Session=Depends(session.get)):
    return db_session.query(models.ListValues).all()

class ColumnParam(BaseModel):
    column: str
    name: str

@router.post('/add')
async def add(
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    add_columndict_params: List[ColumnParam] = Body(
        ...,
        example=[{"column": "series", "name": "日本たばこ産業株式会社"}]
    )
):
    try:
        for add_columndict_param in add_columndict_params:
            add_column = models.ListValues()
            add_columndict_param_dict = add_columndict_param.dict()
            for key, value in add_columndict_param_dict.items():
                if hasattr(add_column, key):
                    setattr(add_column, key, value)
            db_session.add(add_column)
            db_session.commit()
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True


@router.post('/update')
async def update(
    db_session: Session=Depends(session.get),
    update_column_params: List[ColumnParam] = Body(
        ...,
        example=[{"id": "0", "column": "series", "name": "セブンスターX"}]
    )
):
    for update_column_param in update_column_params:
        update_column_param_dict = update_column_param.dict()
        update_column = db_session.query(models.ListValues).filter(models.ListValues.code == update_column_param_dict['code']).all()[0]
        for key, value in update_column_param_dict.items():
            if key != 'code' and hasattr(update_column, key):
                setattr(update_column, key, value)
        db_session.commit()

    try:
        pass
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True

@router.post('/delete')
async def delete(
    db_session: Session=Depends(session.get),
    delete_column_params: List[ColumnParam] = Body(
        ...,
        example=[{"id": "2"}]
    )
):
    for delete_column_param in delete_column_params:
        delete_column_param_dict = delete_column_param.dict()
        db_session.query(models.ListValues).filter(models.ListValues.code == delete_column_param_dict['code']).all()[0].delete()
        db_session.commit()

    try:
        pass
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True
