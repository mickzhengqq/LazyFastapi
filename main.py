# -*- coding: utf-8 -*-
"""main.py"""

from fastapi import FastAPI, Query  #接口服务
from fastapi.middleware.cors import CORSMiddleware #跨域
from routers import router1
from fastapi.openapi.docs import (
     get_redoc_html,
     get_swagger_ui_html,
     get_swagger_ui_oauth2_redirect_html,
 )
from fastapi.staticfiles import StaticFiles  #need install
#need python>=3.7
import uvicorn  #need install
import os

import json
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

import pandas as pd  #need install
import datetime

print('os.getcwd():',os.getcwd())
from config import get_conn as get_conn

#创建App
app = FastAPI()
#配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件位置
static_dir = os.path.dirname(os.path.abspath(__file__))
print('static_dir',static_dir)
app.mount("/api/static", StaticFiles(directory=f"{static_dir}/static"), name="static")
app.include_router(router1.router)

#全量表
@app.get('/api/{table}/',tags=["common"])
def query(table:str):
    try:
        conn = get_conn()
        df = pd.read_sql_query(f'select * from {table}', conn)
        #df = pd.read_sql(f'select * from {table}', engine)
        conn.close()
        if 'dt' in df.keys():df['dt']=df['dt'].astype(str)
        dj = df.to_json(orient='records',force_ascii = False).replace('"[','[').replace(']"',']')
        return {
            "code":200,
            "data": json.loads(dj)
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

@app.get('/api/{table}/{field}',tags=["common"])
def query_parm(table:str,field:str='',sort:str='',search_column='school_name',search_key:str=''):
    try:
        if '=' in field: 
            str_filter = 'where '+' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
        else:
            str_filter = 'where 1=1 '
        if search_key != '':
            str_filter = str_filter + " and {} like '%{}%'".format(search_column,search_key)
        str_sort = f" order by {sort}" if sort != "" else ""
        conn = get_conn()
        if str_filter=='where ':str_filter = str_filter + ' 1=1'
        df = pd.read_sql_query(f'select * from {table} {str_filter} {str_sort}', conn)
        conn.close()
        if 'dt' in df.keys():df['dt'] = df['dt'].astype(str)
        dj = df.to_json(orient='records',force_ascii = False)
        return {
            "code":200,
            "data": json.loads(dj)
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

#取n天内数据\m个月内数据(每隔5m天) /apidt/table/field?cnt=xx&unit=xxx
period_map={
'最近一周':('6','day'),
'最近1周':('6','day'),
'最近14天':('13','day'),
'最近1个月':('1','month'),
'本月':('1','month'),
'最近一个月':('1','month'),
'最近3个月':('3','month'),
'最近三个月':('1','month'),
'最近半年':('6','month'),
'本学期':('6','month'),
'最近1年':('12','month'),
'最近一年':('12','month'),
'本学年':('12','month'),}
@app.get('/api/dt/{table}/{field}',tags=["common"])
def query_parm2(table:str,field:str='',v:str='',cnt:int=7,unit:str='day',period:str='最近1周'):
    try:
        if not period in period_map.keys():period='最近1周'
        cnt,unit = period_map[period]
        unit = unit if unit == 'day' else 'month'
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        begin_day = f'DATE_SUB(\'{today}\',INTERVAL {cnt} {unit})'
        if '=' in field: 
            str_filter = 'where ' +' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
        elif v != '':
            str_filter = ' where {}=\'{}\''.format(field, v) if field != '' else ''
        if unit == 'day':
            dt_filter = f' and dt>={begin_day} and dt<=\'{today}\' '
        elif unit == 'month':
            dt_filter = f'  and dt>={begin_day} and dt<=\'{today}\' ' # and (dt = \'{today}\' or DATEDIFF(dt,{begin_day})%({cnt}*5)=0)'
        str_filter = str_filter + dt_filter
        #return {"sql":str_filter}
        conn = get_conn()
        df = pd.read_sql_query(f'select * from {table} {str_filter}', conn)
        conn.close()
        if 'dt' in df.keys():df['dt']=df['dt'].astype(str)
        dj = df.to_json(orient='records',force_ascii = False)
        return {
            "code":200,
            "data": json.loads(dj)
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

#接口测试BEGIN
@app.get('/test/{table}',tags=["test"])
def test(table:str ,q: str = Query(None, max_length=5)):
    try:
        #res = db.execute(f'select * from {table}')
        #lines = res.fetchall()
        #columns = [col for col in res.keys()]
        return {
            "code":200,
            "msg":"查询表格{}全部数据".format(table),
            "data": f'select * from {table}'
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)
    
@app.get('/test/{table}/{field}',tags=["test"])
def test2(table:str ,field:str,search_column='school_name',search_key:str=''):
    try:
        conn = get_conn()
        columns = list(pd.read_sql_query('select column_name from information_schema.COLUMNS where table_name="area_student_academic_testing_rate"',conn)['column_name'])
        #res = db.execute(f'select * from {table}')
        #lines = res.fetchall()
        #columns = [col for col in res.keys()]
        if '=' in field: 
            str_filter = 'where '+' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
        else:
            str_filter = ' where 1=1'
        if search_key != '':
            str_filter = str_filter + " and {} like '%{}%'".format(search_column,search_key)
        return {
            "code":200,
            "msg":f'select * from {table} {str_filter}'
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

@app.get('/test/tables',tags=["test"])
def test3():
    try:
        #res = db.execute('show tables')
        #lines = res.fetchall()
        #columns = [col for col in res.keys()]
        conn = get_conn()
        df = pd.read_sql_query('show tables', conn)
        conn.close()
        dj = df.to_json(orient='records',force_ascii = False)
        return {
            "code":200,
            "msg":"查询表",
            "data": json.loads(dj)
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

#----------#接口测试END
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8008, reload=True)