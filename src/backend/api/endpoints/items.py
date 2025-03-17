from pyexpat import model
from fastapi import APIRouter, Request, Body, Depends
from sqlalchemy.sql.sqltypes import Boolean
from db import session, models, crud
import sqlalchemy
from sqlalchemy import and_, between, or_, text, func
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from pydantic import BaseModel
from typing import List
from typing import Optional
from sqlalchemy.sql import func
import datetime
from api.endpoints import auth


router = APIRouter()

# 全Itemを返すエンドポイント
@router.get('/all')
def get_items(db_session: Session=Depends(session.get)):
    return db_session.query(models.MainItems).all()


@router.get('/all_column')
def get_items(db_session: Session=Depends(session.get)):
    items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=session.engine)
    return items_table.c.keys()


@router.post('/search')
async def search_items(
    # request: Request,
    db_session: Session=Depends(session.get),
    search_item_params = Body(
        ...,
        example=[
            {'name': 'セブン'}
        ]
    ),
):
    items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=session.engine)
    items_table = db_session.query(items_table).filter(items_table.columns.name.like('%'+search_item_params[0]['name']+'%')).all()
    return items_table


# 条件でフィルタしたItemを返すエンドポイント
@router.post('/filter')
async def filter_items(
    # request: Request,
    db_session: Session=Depends(session.get),
    search_item_params = Body(
        ...,
        example=[
            {
                'name': 'ボックス',
                'series': ['セブンスター'],
                'nicotine': ["1~1.2"],
                'release_date': ['2023-2-1~2023-2-8']
            }
        ]
    ),
):
    filter_params = []
    print(search_item_params)
    for search_item_param in search_item_params:
        and_filter_params = []
        for key, values in search_item_param.items():
            or_filter_params = []
            if isinstance(values, str):
                or_filter_params.append(getattr(models.MainItems, key).like(f'%{values}%'))
            else:
                for or_value in values:
                    if '~' in or_value:
                        try:
                            or_filter_params.append(and_(
                                getattr(models.MainItems, key)>=datetime.datetime.strptime(or_value.split('~')[0], '%Y-%m-%d').date(),
                                getattr(models.MainItems, key)<=datetime.datetime.strptime(or_value.split('~')[1], '%Y-%m-%d').date()
                            ))
                        except:
                            or_filter_params.append(getattr(models.MainItems, key).between(*or_value.split('~')))
                    else:
                        or_filter_params.append(getattr(models.MainItems, key) == or_value)
            and_filter_params.append(or_(*or_filter_params))
        filter_params.append(and_(*and_filter_params))
    return db_session.query(models.MainItems).filter(and_(*filter_params)).all()


# Item追加用エンドポイント
@router.post('/add')
async def add(
    # request: Request,
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    add_item_params = Body(
        ...,
        example=[
            {'name': 'ピアニッシモ・アリア・メンソール', 'discription': 'ピアニッシモ（PIANISSIMO）は、たばこの銘柄の一つ。日本では日本たばこ産業（JT）から製造・販売されている。', 'price': '540', 'amount': '20', 'nicotine': '0.1', 'tar': '1'}
        ]
    ),
):
    for add_item_param in add_item_params:
        items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=session.engine)
        if not db_session.query(items_table).filter_by(name=add_item_param['name']).all():
            item_insert = sqlalchemy.insert(items_table).values(add_item_param)
            db_session.execute(item_insert)
            db_session.commit()

    try:
        pass
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True


# Item更新用エンドポイント
@router.post('/update')
async def update(
    # request: Request,
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    update_item_params = Body(
        ...,
        example=[
            {'id': '3', 'name': 'ピアニッシモ・アリア・メンソール', 'discription': '楽しい彩りを味わおう。\nフルーティに香る、ミントフレーバーメンソール', 'price': '540', 'amount': '20', 'nicotine': '0.1', 'tar': '1', 'release_date': '2000-01-01'}
        ]
    ),
):
    for update_item_param in update_item_params:
        items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=session.engine)
        update_item_dict = {}
        for column_code, column_value in update_item_param.items():
            update_item_dict[column_code] = column_value
            try:
                update_item_dict[column_code] = datetime.datetime.strptime(column_value, '%Y-%m-%d')
                # update_item_dict[column_code] = datetime.datetime.now()
            except:
                update_item_dict[column_code] = column_value
        print(update_item_dict)
        item_update = sqlalchemy.update(items_table).filter_by(id=update_item_param['id']).values(update_item_dict)
        db_session.execute(item_update)
        db_session.commit()
    try:
        pass
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True



# Item削除用エンドポイント
@router.post('/delete')
async def delete(
    # request: Request,
    current_user: auth.User = Depends(auth.get_current_active_user),
    db_session: Session=Depends(session.get),
    delete_item_params = Body(
        ...,
        example=[
            {'id': '3'}
        ]
    ),
):
    for delete_item_param in delete_item_params:
        items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=session.engine)
        # print(db_session.query(items_table).filter_by(name = delete_item_param['name']).all())
        db_session.query(items_table).filter_by(id = delete_item_param['id']).delete()
        db_session.commit()
    try:
        pass
    except:
        db_session.rollback()
        print('add_column_faild')
        return False
    return True









