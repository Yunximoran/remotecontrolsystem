

class MYEXCEPTION(Exception):
    pass


class NODEERROR(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class RESOLVERERROR(Exception):
    def __init__(self, *args):
        super().__init__(*args)