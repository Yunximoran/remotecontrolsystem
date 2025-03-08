from fastapi import APIRouter, HTTPException

from gloabl import DB
from datamodel import (
    Credentils,
    NewUser
)

# 用户接口
router = APIRouter()
prefix = "/server/login"
tags = ["login"]


@router.post("/{id}")
async def login(credentils: Credentils):
    """
        用户登录
        
    credentils: 用户凭证
    """
    # 解析账号&密码
    credentils = credentils.account
    password = credentils.password
    
    # 从redis中获取所有用户
    accounts_information = DB.hget("accounts", credentils)
    # 校验用户是否存在
    if accounts_information is not None:
        # 校验用户密码是否正确
        if password == accounts_information['password']:
            # 返回用户信息
            return {"start": "OK", "msg": accounts_information}
        else:
            # 返回密码错误是信息
            raise HTTPException(status_code=404, detail="password is error")
    else:
        # 返回用户不存在是信息
        raise HTTPException(status_code=404, detail="account is not exits")
    

@router.post("/registry")
async def registryaccount(regisform: NewUser):
    """
        注册新用户
    regisform: 注册表单
    """
    # 将表单写入redis数据库
    DB.hset("accounts", regisform.account, regisform.model_dump_json())   
    return {
        "account": regisform.account,
        "username": regisform.username
    }