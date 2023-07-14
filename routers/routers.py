from fastapi import APIRouter

#创建一个路由
router = APIRouter()

#导入子路由
from .common import router as common
from .test import router as test

router.include_router(common)
router.include_router(test)


