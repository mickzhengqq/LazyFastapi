# LazyFastapi README
# 目录说明
server.py 导入routers.routers路由，routers导入其他子路由。
开发时，添加其他子路由文件，编辑routers.py添加其他路由名称。
运行时直接更新 routers/routers.py 和其他子路由文件。

# 执行
nohup python3 main.py > ./main.log 2>&1 &

# docs
http://localhost:8008/docs