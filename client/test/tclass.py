class World:
    def __init__(self, countries):
        self.countries = countries
    
    def __getattr__(self, key):
        print(f"__getattr__ called: unexisted key {key}")
        return None
    
    def __getattribute__(self, key):
        print(f"__getattribute__ called: key {key}")
        return super(World, self).__getattribute__(key)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            print(f"__setattr__ called: key existed {key}")
        else:
            print(f"__setattr__ called: key unexisted {key}")
        self.__dict__[key] = value
    
    def __delattr__(self, key):
        print(f"__delattr__ called: key {key}")
        del self.__dict__[key]

w = World(256)
w.oceans = 5
del w.countries
"""
deepseek api key: sk-be83a1d93d1d4e05afd15e3ca6b3d5a9
Output:
# __getattribute__ called: key __dict__
#__setattr__ called: key unexisted countries
# __getattribute__ called: key __dict__

# __getattribute__ called: key __dict__
# __setattr__ called: key unexisted oceans
# __getattribute__ called: key __dict__

# __delattr__ called: key countries
# __getattribute__ called: key __dict__
"""

