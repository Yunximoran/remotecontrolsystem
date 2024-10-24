from typing import Annotated
from pydantic import BaseModel

from .heart_pkgs import HeartPkgs
from .software_checklist import SoftWareCheckList, SoftWare



class ShellList(BaseModel):
    name: Annotated[str, None]
    shell: Annotated[str, None]