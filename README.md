# LazyFastapi README
# Version:1.2 mickzheng@qq.com

# 目录说明
/README.md           //项目说明文件
/server.py           //启动接口应用，提供静态资源接口和导入路由
/apiserver_main.sh   //启动脚本，启动并写入日志
/config.py           //数据库连接配置
/routers             //存放路由文件
/routers/common.py   //公共的接口，包括全表查询、带条件查询、模糊搜索查询
/routers/router.py   //公用的路由基础模块，可以被子路由文件引用
/routers/routers.py  //路由文件，用来导入子路由
/routers/test.py     //测试接口，包括查询库有哪些表、接口sql
/static              //静态文件
/static/demo         //测试文件，访问路径  http://localhost:8008/api/static/demo
/static/6.gif        //测试文件，访问路径  http://localhost:8008/api/static/6.gif

使用前修改 config.py
在/routers里添加路由文件后，在/routers/routers添加引用。

# 执行
nohup python3 main.py > ./main.log 2>&1 &

# docs
http://localhost:8008/docs
