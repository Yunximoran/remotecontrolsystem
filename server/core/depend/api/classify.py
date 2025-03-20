from fastapi import APIRouter


router = APIRouter()
prefix = "server/classify"
tag = ["classify"]

@router.put("/add")
async def addsoftware(self):
    pass

@router.put("/pop")
async def popsoftware(self):
    pass

@router.post("/start")
async def start(self):
    pass

@router.post("/close")
async def close(self):
    pass