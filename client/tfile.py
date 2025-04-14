from lib import Resolver


with Resolver() as r:
    path = r("local")
    data = path.search("data")
    
    print(data.path)
    print(data.files['softwares.json'])