from fastapi import APIRouter, HTTPException

from databasetool import Redis
from datamodel import (
    Credentils,
    NewUser
)

# 用户接口
router = APIRouter()
prefix = "/server/login"
tags = ["login"]


@router.post("/{id}")
async def login(loginform: Credentils):
    credentils = loginform.account
    password = loginform.password
    accounts_information = Redis.hget("accounts", credentils)
    if accounts_information is not None:
        if password == accounts_information['password']:
            return {"start": "OK", "msg": accounts_information}
        else:
            raise HTTPException(status_code=404, detail="password is error")
    else:
        raise HTTPException(status_code=404, detail="account is not exits")
    

@router.post("/registry")
async def registryaccount(regisform: NewUser):
    # 注册新用户，保存在数据库
    Redis.hset("accounts", regisform.account, regisform.model_dump_json())   
    return {
        "account": regisform.account,
        "username": regisform.username
    }