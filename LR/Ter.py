class Ter:
    def __init__(self,val):
        self.val = val

    def __str__(self):
        return 'id'



class NonTer:
    def __init__(self,alpha):
        self.val=None
        self.alpha = alpha
        self.posi:dict=None

    def __str__(self):
        return self.alpha