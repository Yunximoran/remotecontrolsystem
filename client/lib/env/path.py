from pathlib import Path
"""
    配置项目结构
"""
# 项目根目录
WORKDIR= Path.cwd()

# local 本地资源地址配置
LOCAL_PATH = Path("local")

LOCAL_DIR_DATA = LOCAL_PATH.joinpath("data")
LOCAL_DIR_LOGS = LOCAL_PATH.joinpath("logs")
LOCAL_DIR_SOFT = LOCAL_PATH.joinpath("soft")
LOCAL_DIR_FILE = LOCAL_PATH.joinpath("file")

PATH_MAP_SOFTWARES = LOCAL_DIR_DATA.joinpath("softwares.json")
PATH_LOG_SHELLS = LOCAL_DIR_DATA.joinpath("shells.json")




__all__ = [
    "LOCAL_DIR_DATA",
    "LOCAL_DIR_LOGS",
    "LOCAL_DIR_SOFT",
    "LOCAL_DIR_FILE",
    "PATH_MAP_SOFTWARES",
    "PATH_LOG_SHELLS",
]
