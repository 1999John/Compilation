import re
class Product:
    def __init__(self,pd:str):
        self._source:str
        self._right:list
        self.parse(pd)
    def parse(self,pd:str):
        self._source = pd[:pd.find('-')]
        right = pd[pd.find('>')+1:]
        self._right = self.parse_right_to_list(right)
        # print(self._source,self._right)
    def parse_right_to_list(self,right:str):
        # 提取出终结符，非终结符
        return re.findall("select|from|where|=|insert into|values|id|create|table|[+*A-Za-z~|][']?|[(),;]|~",right)
        # todo: util的正则表达式
    @property
    def source(self):
        return self._source
    @property
    def right(self):
        return self._right

    def __str__(self) -> str:
        right = ""
        for i in self._right:
            right += str(i)
        return self._source+'->'+right


if __name__=='__main__':
    pd = "A->(B)BC'idc|~"
    p = Product(pd)
    print(p)