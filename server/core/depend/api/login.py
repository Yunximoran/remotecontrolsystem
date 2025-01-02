from fastapi import APIRouter, HTTPException

from databasetool import DataBaseManager as DATABASE
from datamodel import (
    Credentils,
    NewUser
)

router = APIRouter()


@router.post("/login/{id}", tags=['login'])
async def login(loginform: Credentils):
    credentils = loginform.account
    password = loginform.password
    accounts_information = DATABASE.hget("accounts", credentils)
    if accounts_information is not None:
        if password == accounts_information['password']:
            return {"start": "OK", "msg": accounts_information}
        else:
            raise HTTPException(status_code=404, detail="password is error")
    else:
        raise HTTPException(status_code=404, detail="account is not exits")
    

@router.put("/login/registry", tags=['registry'])
async def registryaccount(regisform: NewUser):
    # 注册新用户，保存在数据库
    DATABASE.hset("accounts", regisform.account, regisform.model_dump_json())   
    return {
        "account": regisform.account,
        "username": regisform.username
    }