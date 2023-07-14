from fastapi import Query  #接口服务
import datetime
import pandas as pd
import json
from dateutil.relativedelta import relativedelta
import os
import sys

#from routers.router import router
from fastapi import APIRouter
router = APIRouter()

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from config import get_conn as get_conn

def get_month(d=0,opformat='{}月'):
    result = opformat.format((datetime.date.today() - relativedelta(months=d)).month)
    return result

#全量表
@router.get('/api/{table}/',tags=["common"])
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

#表查询过滤
@router.get('/api/{table}/{field}',tags=["common"])
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

# #取n天内数据\m个月内数据(每隔5m天) /apidt/table/field?cnt=xx&unit=xxx
# period_map={
# '最近一周':('6','day'),
# '最近1周':('6','day'),
# '最近14天':('13','day'),
# '最近1个月':('1','month'),
# '本月':('1','month'),
# '最近一个月':('1','month'),
# '最近3个月':('3','month'),
# '最近三个月':('1','month'),
# '最近半年':('6','month'),
# '本学期':('6','month'),
# '最近1年':('12','month'),
# '最近一年':('12','month'),
# '本学年':('12','month'),}
# @router.get('/api/dt/{table}/{field}',tags=["common"])
# def query_parm2(table:str,field:str='',v:str='',cnt:int=7,unit:str='day',period:str='最近1周'):
#     try:
#         if not period in period_map.keys():period='最近1周'
#         cnt,unit = period_map[period]
#         unit = unit if unit == 'day' else 'month'
#         today = datetime.datetime.now().strftime('%Y-%m-%d')
#         begin_day = f'DATE_SUB(\'{today}\',INTERVAL {cnt} {unit})'
#         if '=' in field: 
#             str_filter = 'where ' +' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
#         elif v != '':
#             str_filter = ' where {}=\'{}\''.format(field, v) if field != '' else ''
#         if unit == 'day':
#             dt_filter = f' and dt>={begin_day} and dt<=\'{today}\' '
#         elif unit == 'month':
#             dt_filter = f'  and dt>={begin_day} and dt<=\'{today}\' ' # and (dt = \'{today}\' or DATEDIFF(dt,{begin_day})%({cnt}*5)=0)'
#         str_filter = str_filter + dt_filter
#         #return {"sql":str_filter}
#         conn = get_conn()
#         df = pd.read_sql_query(f'select * from {table} {str_filter}', conn)
#         conn.close()
#         if 'dt' in df.keys():df['dt']=df['dt'].astype(str)
#         dj = df.to_json(orient='records',force_ascii = False)
#         return {
#             "code":200,
#             "data": json.loads(dj)
#         }
#     except Exception as e:
#         resu = {'code': -1, 'msg': e.__str__}
#         return json.dumps(resu,ensure_ascii=False)

# #月份按当前月份往前计算
# @router.get("/router/dt/{table}/{field}",tags=["router"])
# def getPeriodData(table:str,field:str='',unit:str='month',opformat:str='{}月'):
#     try:
#         if '=' in field: 
#             str_filter = 'where '+' and '.join(['{}=\'{}\''.format(f.split('=')[0],f.split('=')[1]) for f in field.split('&')])
#         else:
#             str_filter = 'where 1=1 '
#         conn = get_conn()
#         if str_filter == 'where ':str_filter = str_filter + ' 1=1'
#         str_sql = f'select * from {table} {str_filter}'
#         df = pd.read_sql_query(str_sql, conn)
#         list_month = list(map(get_month,range(df.shape[0]-1,-1,-1)))
#         df['month'] = list_month
#         dj = df.to_json(orient='records',force_ascii = False)
#         return {
#             "code":200,
#             "data": json.loads(dj)
#         }
#     except Exception as e:
#         resu = {'code': -1, 'msg': e.__str__}
#         return json.dumps(resu,ensure_ascii=False)


