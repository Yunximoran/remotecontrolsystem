from pydantic import BaseModel
from typing import Annotated, Optional,  AnyStr
from fastapi import Query

from lib.strtool import pattern


class ClassTable(BaseModel, frozen=True):
    soft: Annotated[str, None]
    ip: Annotated[str, None] = Query(pattern=pattern.IP)
    
class Classify(BaseModel):
    name: Annotated[AnyStr, None]
    items: Optional[set[ClassTable]]
    
