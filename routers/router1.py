#from fastapi import Body #, Header, Form
from fastapi import APIRouter
import os
import sys
import pandas as pd
import json
from dateutil.relativedelta import relativedelta
import datetime

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from config import get_conn as get_conn

router = APIRouter()

def get_month(d=0,opformat='{}月'):
    result = opformat.format((datetime.date.today() - relativedelta(months=d)).month)
    return result

#月份按当前月份往前计算
@router.get("/api/router1/dt/{table}/{field}",tags=["router1"])
def getPeriodData(table:str,field:str='',unit:str='month',opformat:str='{}月'):
    try:
        if '=' in field: 
            str_filter = 'where '+' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
        else:
            str_filter = 'where 1=1 '
        conn = get_conn()
        if str_filter == 'where ':str_filter = str_filter + ' 1=1'
        str_sql = f'select * from {table} {str_filter}'
        df = pd.read_sql_query(str_sql, conn)
        list_month = list(map(get_month,range(df.shape[0]-1,-1,-1)))
        df['month'] = list_month
        dj = df.to_json(orient='records',force_ascii = False)
        return {
            "code":200,
            "data": json.loads(dj)
        }
    except Exception as e:
        resu = {'code': -1, 'msg': e.__str__}
        return json.dumps(resu,ensure_ascii=False)

#通用接口
@router.get('/api/router1/common/{table}/{field}',tags=["router1"])
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
