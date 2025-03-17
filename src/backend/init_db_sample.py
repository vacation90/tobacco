# -*- coding: utf-8 -*-
from datetime import datetime
import os
import random
from tempfile import gettempdir
import time
import logging
from statistics import mode
from numpy import product
import sqlalchemy
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.operations import Operations

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

# print(random_date("1/1/2008 1:30 PM", "1/1/2009 4:50 AM", random.random()))


alembic_cfg = Config('alembic.ini')
print(command.history(alembic_cfg))
print(command.branches(alembic_cfg))
print('current')
print(command.current(alembic_cfg))
print('---')
print(bool(command.current(alembic_cfg)))

print('downgrade')
print(command.downgrade(alembic_cfg, 'base'))
print(command.current(alembic_cfg))
try:
    print('revision')
    print(command.revision(alembic_cfg, autogenerate = True, message = 'initialize'))
    print(command.upgrade(alembic_cfg, 'head'))
except:
    logging.exception('')
    print('upgrade+1')
    print(command.upgrade(alembic_cfg, '+1'))

# print(command.stamp(alembic_cfg, "head"))

# session.Base.metadata.drop_all(session.engine)
# session.Base.metadata.create_all(session.engine)

from db import models
# from db import base, session, models
# from sqlalchemy.ext.automap import automap_base
import requests as rq
from lxml import html
from bs4 import BeautifulSoup
import re


db_session = models.session.SessionLocal()
print(models.session.engine.has_table('columns'))
print(db_session.query(models.Columns).all())

add_user_params = [
    {'email': 'johndoe@jp', 'hashed_password': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'is_active': True},
]

for add_user_param in add_user_params:
    add_user = models.Users()
    for key, value in add_user_param.items():
        if hasattr(add_user, key):
            setattr(add_user, key, value)
    db_session.add(add_user)
    db_session.commit()


add_column_params = [
    {'code': 'name', 'name': '銘柄', 'data_type': 'text', 'default_value': '',},
    {'code': 'series', 'name': 'シリーズ', 'data_type': 'text', 'default_value': '', },
    {'code': 'discription', 'name': '概要', 'data_type': 'text', 'default_value': '', },
    {'code': 'image', 'name': '画像', 'data_type': 'image', 'default_value': '', },
    {'code': 'sale_url', 'name': '販売先URL', 'data_type': 'url', 'default_value': '', },
    {'code': 'price', 'name': '価格', 'data_type': 'int', 'default_value': '0', },
    {'code': 'amount', 'name': '数量', 'data_type': 'int', 'default_value': '0', },
    {'code': 'nicotine', 'name': 'ニコチン', 'data_type': 'num', 'default_value': '0.0', 'unit': 'mg',},
    {'code': 'tar', 'name': 'タール', 'data_type': 'num', 'default_value': '0.0', 'unit': 'mg',},
    {'code': 'release_date', 'name': '発売日', 'data_type': 'date', 'default_value': ''},
]

for add_column_param in add_column_params:
    if not db_session.query(models.Columns).filter_by(code = add_column_param['code']).scalar():
        print('add')
        add_column = models.Columns()
        for key, value in add_column_param.items():
            print(key, value)
            if hasattr(add_column, key):
                setattr(add_column, key, value)
        db_session.add(add_column)
        db_session.commit()
        if not hasattr(models.MainItems, add_column_param['code']):
            print('add_column.sql_data_type: ', add_column.sql_data_type())
            # print(type(getattr(models.Columns, 'code')), getattr(models.Columns, 'code'))
            # setattr(models.MainItems, add_column_param['code'], getattr(sqlalchemy, add_column.sql_data_type()))
            setattr(models.MainItems, add_column_param['code'], sqlalchemy.Column(add_column.sql_data_type()))
            print(type(getattr(models.MainItems, add_column_param['code'])), getattr(models.MainItems, add_column_param['code']))
        else:
            print('not models.MainItems')
            print(models.MainItems)
            print(getattr(models.MainItems, add_column_param['code']))

for c in db_session.query(models.Columns).all():
    print(c.code, c.name)

print(dir(models.MainItems.price))
for a in dir(models.MainItems.price):
    if not '_' in a:
        print(a, getattr(models.MainItems.price, a))
print(type(models.Columns.code))
print(type(models.MainItems.id))
print(models.MainItems.name)
print(command.current(alembic_cfg))
print('---------')
try:
    print(command.revision(alembic_cfg, autogenerate = True, message = 'add column'))
    print(command.upgrade(alembic_cfg, 'head'))
except:
    pass

items_table = sqlalchemy.Table(models.MainItems.__tablename__, sqlalchemy.MetaData(), autoload_with=models.session.engine)
print(items_table.c.keys())

try:
    pass
except:
    db_session.rollback()
    print('column faild')


print('----------------------------')
print(db_session.query(models.MainItems))
# print(db_session.query(models.MainItems).add_column(sqlalchemy.Column(sqlalchemy.String(255))))


add_columndict_params = []
add_item_params = []
for i in range(1, 71):
    # print('------------------------------------')
    print('page: ', i)
    res = rq.get(f'https://tabaco-ex.ocnk.net/product-list/{i}/0/normal?num=1000&img=200&sort=')
    soup = BeautifulSoup(res.text, 'html.parser')
    if soup.select('div.item_data.clearfix'):
        series = soup.select('div.page_title > h2')[0].text.replace('\n', '').replace(' ', '')

        add_columndict_params.append({
            'column': 'series',
            'name': series,
        })

        for item_soup in soup.select('div.item_data.clearfix'):
            # print(item_soup.select('span.goods_name')[0].text)
            name = item_soup.select('span.goods_name')[0].text
            image_url = item_soup.select('div.global_photo img')[0]['src']
            save_path = image_url.replace('https://', '')
            item_desc = item_soup.select('p.item_desc')[0].text
            amount_match = re.search(r'入数/(\d+)個 ： 20本', item_desc)
            nicotine_match = re.search(r'ニコチン ： ([\d\.]+)mg', item_desc)
            tar_match = re.search(r'タール ： ([\d\.]+)mg', item_desc)

            if not os.path.isfile('../frontend/public/'+save_path):
                os.makedirs(os.path.dirname('../frontend/public/'+save_path), exist_ok=True)
                print('save: ../frontend/public/'+save_path)
                with open('../frontend/public/'+save_path, 'wb') as f:
                    f.write(rq.get(image_url).content)

            add_item_params.append({
                'name': name,
                'series': series,
                'image': './'+save_path,
                'sale_url': f'https://tabaco-ex.ocnk.net/product-list/{i}',
                'discription': f'{name}の情報です',
                'price': int(item_soup.select('span.figure')[0].text.replace(',', '').replace('円', '')),
                'amount': int(amount_match[1]) if amount_match else 0,
                'nicotine': float(nicotine_match[1]) if nicotine_match else 0,
                'tar': float(tar_match[1]) if tar_match else 0,
                'release_date': datetime.now().date()
            })


for add_item_param in add_item_params:
    mainitems = models.MainItems()
    for key, value in add_item_param.items():
        if hasattr(mainitems, key):
            setattr(mainitems, key, value)
    db_session.add(mainitems)
    db_session.commit()


print(add_columndict_params)
# print(add_item_params)



# # add_columndict_params = [
# #     {'column': 'series', 'name': 'セブンスター'},
# #     {'column': 'series', 'name': 'メビウス'},
# #     {'column': 'series', 'name': 'ラーク'},
# # ]

try:
    for add_columndict_param in add_columndict_params:
        add_column = models.ListValues()
        add_columndict_param_dict = add_columndict_param
        for key, value in add_columndict_param_dict.items():
            if hasattr(add_column, key):
                setattr(add_column, key, value)
        db_session.add(add_column)
        db_session.commit()
except:
    db_session.rollback()
    print('listvalue faild')


# # add_item_params = [
# #     {'name': 'セブンスター', 'series': 'セブンスター', 'image': 'https://tabaco-ex.ocnk.net/data/tabaco-ex/product/20210206_774f14.jpg', 'discription': 'セブンスター（Seven Stars、一部ボックスはSEVEN STARS表記）は、日本たばこ産業（JT）から製造・販売されている日本の代表的なたばこの銘柄の一つで、JTの主力銘柄のひとつ。', 'price': '600', 'amount': '20', 'nicotine': '1.2', 'tar': '14.0'},
# #     {'name': 'セブンスター・ボックス', 'series': 'セブンスター', 'image': 'https://tabaco-ex.ocnk.net/data/tabaco-ex/product/20210209_fd9d6b.jpg', 'discription': 'セブンスター（Seven Stars、一部ボックスはSEVEN STARS表記）は、日本たばこ産業（JT）から製造・販売されている日本の代表的なたばこの銘柄の一つで、JTの主力銘柄のひとつ。', 'price': '600', 'amount': '20', 'nicotine': '1.2', 'tar': '14'},
# #     {'name': 'セブンスター・メンソール・１２・ボックス', 'series': 'セブンスター', 'image': 'https://tabaco-ex.ocnk.net/data/tabaco-ex/product/20210209_e706e1.jpg', 'discription': 'セブンスター（Seven Stars、一部ボックスはSEVEN STARS表記）は、日本たばこ産業（JT）から製造・販売されている日本の代表的なたばこの銘柄の一つで、JTの主力銘柄のひとつ。', 'price': '600', 'amount': '20', 'nicotine': '1.0', 'tar': '12'},
# #     {'name': 'メビウス', 'series': 'メビウス', 'image': 'https://tabaco-ex.ocnk.net/data/tabaco-ex/product/20210208_809ccb.jpg', 'discription': 'メビウス（MEVIUS）は、日本たばこ産業（JT）が1977年6月から製造・販売しているたばこの銘柄の一つで、JTの最主力銘柄である。2013年1月まではマイルドセブン（MILD SEVEN）の名称で販売されていた。外箱のコンセプトカラーは水色。常にブランド拡大を行うことで、ファミリーシェアナンバーワンを保持している。JT製品ファミリーの中で最も銘柄数が多い。', 'price': '540', 'amount': '20', 'nicotine': '0.8', 'tar': '10'},
# #     {'name': 'メビウス・ボックス', 'series': 'メビウス', 'image': 'https://tabaco-ex.ocnk.net/data/tabaco-ex/product/20210208_a82479.jpg', 'discription': 'メビウス（MEVIUS）は、日本たばこ産業（JT）が1977年6月から製造・販売しているたばこの銘柄の一つで、JTの最主力銘柄である。2013年1月まではマイルドセブン（MILD SEVEN）の名称で販売されていた。外箱のコンセプトカラーは水色。常にブランド拡大を行うことで、ファミリーシェアナンバーワンを保持している。JT製品ファミリーの中で最も銘柄数が多い。', 'price': '540', 'amount': '20', 'nicotine': '0.8', 'tar': '10'},
# # ]


# for add_item_param in add_item_params:
#     add_item_param_dict = add_item_param
#     Base = automap_base()
#     Base.prepare(session.engine, reflect=True)
#     AutomapMainItems = Base.classes.mainitems
#     automap_mainitems = AutomapMainItems()
#     for key, value in add_item_param_dict.items():
#         if hasattr(automap_mainitems, key):
#             setattr(automap_mainitems, key, value)
#     db_session.add(automap_mainitems)
#     db_session.commit()




# try:
#     pass



# except:
#     db_session.rollback()
#     db_session.close()
#     print('add_column_faild')

# db_session.close()