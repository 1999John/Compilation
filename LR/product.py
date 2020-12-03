import re
from . import *
class Product:
    def __init__(self,product:str):
        self.right:list
        self.left:str
        self._parse_str_to_Product(product)
        for _ in range(self.right.count('')):
            self.right.remove('')

    def _parse_str_to_Product(self,product:str):
        self.left = product[:product.index('->')]
        self.right = self._parse_right_to_list(product[product.index('->')+2:])
    def _parse_right_to_list(self,right:str):
        return re.findall(pattern_all,right)

    def __eq__(self, o: object) -> bool:
        if self.left!=o.left:
            return False
        if len(self.right)!=len(o.right):
            return False

        for l1,l2 in zip(self.right,o.right):
            if l1!=l2:
                return False
        return True

    def __str__(self) -> str:
        ret = self.left+"->"
        for s in self.right:
            ret+=s
        return ret


    def copy(self):
        p = Product(self.__str__()[:])
        p.right = self.right[:]
        return p


