# -*- coding: utf-8 -*-
"""main.py"""

from fastapi import FastAPI, Query  #接口服务
from fastapi.middleware.cors import CORSMiddleware #跨域
from routers import routers
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
# import pandas as pd  #need install
# import datetime

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

#导入路由（总）
app.include_router(routers.router, prefix="/api") #



#----------#接口测试END
if __name__ == '__main__':
    uvicorn.run(app='server:app', host='0.0.0.0', port=8008, reload=True)