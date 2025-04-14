from pathlib import Path


LOCAL_PATH = Path("local")

LOCAL_DIR_DATA = LOCAL_PATH.joinpath("data")
LOCAL_DIR_LOGS = LOCAL_PATH.joinpath("logs")
LOCAL_DIR_SOFT = LOCAL_PATH.joinpath("soft")
LOCAL_DIR_FILE = LOCAL_PATH.joinpath("file")

PATH_MAP_SOFTWARES = LOCAL_DIR_DATA.joinpath("softwares.json")
PATH_LOG_SHELLS = LOCAL_DIR_DATA.joinpath("shells.json")