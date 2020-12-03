class FF:
    def __init__(self,source):
        self.source = source
        self.add = []
        self.first = []
        self.follow = []


    def reset_add(self):
        self._add=[]

    def __str__(self):
        fi,fol="",""
        for f in self.first:
            fi+= f
        for fo in self.follow:
            fol += fo
        return "First({}):".format(self.source)+fi+"\nFollow({}):".format(self.source)+fol