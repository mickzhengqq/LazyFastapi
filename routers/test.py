from fastapi import Query  #接口服务
import datetime
import pandas as pd
import json
#from dateutil.relativedelta import relativedelta
#import os
#import sys

from config import get_conn as get_conn

#from routers.router import router
from fastapi import APIRouter
router = APIRouter()

#接口测试BEGIN
@router.get('/test/{table}',tags=["test"])
def testQueryTableAll(table:str ,q: str = Query(None, max_length=5)):
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
    
@router.get('/test/{table}/{field}',tags=["test"])
def testQueryTable(table:str ,field:str,search_column='school_name',search_key:str=''):
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

@router.get('/test/tables',tags=["test"])
def queryTables():
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