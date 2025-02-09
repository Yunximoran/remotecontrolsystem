from fastapi import APIRouter

# 修改接口
router = APIRouter()
prefix = "/server/alter"
tags = ["alter"]

# 修改设置选项
@router.put("/settings/port/")
async def alter_settings(option: str, nval: str):
    # 修改服务端配置
    """
    option: 选型
    nval: 新值
    """
    return {"ok": f"reset {option} => {nval}"}