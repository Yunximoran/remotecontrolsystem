from pathlib import Path
import yaml

WORKDIR = Path.cwd()

class Resolver:
    """
        配置文件解析器
    """
    CONF = {}
    def __init__(self, filepath):
        self.__conf = Path(filepath)

    
    def __deepparsing(self, node="root"):
        """
            递归读取数据，默认根节点开始读取
        """
        pass
    

if __name__ == "__main__":
    print(Path(WORKDIR).joinpath("docker-compose.yml"))
    with open(Path(WORKDIR).joinpath("docker-compose.yml"), 'r', encoding="utf-8") as f:
        res = yaml.load(f.read(), Loader=yaml.FullLoader)
        print(res)
    
    # print(WORKDIR)
        