
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


from databasetool import DataBaseManager as DB
from projectdesposetool import ProjectManage
from core.depend.api import (
    data,
    send,
    alter,
    login,
    event
)


# CORS
ORIGINS = [
    # vue address
    "https://localhost:8080",
    "http://localhost:8080",
]

PROJECTMANAGE = ProjectManage()

@asynccontextmanager
async def lifespan(app: FastAPI):
    PROJECTMANAGE.loaddata(DB)
    yield
    PROJECTMANAGE.savedata(DB, "heart_packages")
    PROJECTMANAGE.savedata(DB, "softwarelist")
        
    DB.shutdown()


app = FastAPI(lifespan=lifespan)


# config
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)
# load router
app.include_router(
    data.router,
    prefix="/servers/data",
    tags=['data']
)

app.include_router(
    send.router,
    prefix="/servers/sends",
    tags=['send']
)

app.include_router(
    alter.router,
    prefix="/servers/alter",
    tags=["alter"]
)
app.include_router(
    login.router,
    prefix="/servers/login",
    tags=["login"]
)
app.include_router(
    event.router,
    prefix="/servers/event",
    tags=["event"]
)


server = uvicorn.Server(uvicorn.Config(app))




