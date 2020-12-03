from .product import *
from .project import *
from .util import *
from . import *
import re
from LL.products import Product as LLProduct
from LL.util import getFirst as Lgenerate_First
def generate_Follow():
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = [Product("E'->E")]
    for i in range(num):
        p = Product(f.readline())
        products.append(p)
    non_ter_list = list(set([p.left for p in products]))

    f ={}
    add = {}
    fi = {}
    for non_ter in non_ter_list:
        f[non_ter] = []
        add[non_ter] = []
        fi[non_ter]=[]
    f["E'"] = ['$']
    for p in products:
        for alpha in range(len(p.right)):
            # 终结符直接加入Follow集
            if alpha + 1 < len(p.right) and re.match(pattern_ter ,p.right[alpha+1]) and re.match("[A-Z]",p.right[alpha]):
                f[p.right[alpha]].append(p.right[alpha+1])
            # 非终结符加入fi集
            elif alpha + 1 < len(p.right) and re.match("[A-Z]",p.right[alpha]) and re.match("[A-Z]",p.right[alpha+1]):
                fi[p.right[alpha]].append(p.right[alpha+1])
            elif alpha == len(p.right)-1 and re.match("[A-Z]",p.right[alpha]):
                add[p.right[alpha]].append(p.left)


    for __ in range(2):
        for _ in range(len(non_ter_list)*2):
            for non_ter in non_ter_list:
                for add_non_ter in add[non_ter]:
                    f[non_ter]+=f[add_non_ter]

        for _ in range(len(non_ter_list)*2):
            for non_ter in non_ter_list:
                for add_non_ter in fi[non_ter]:
                    f[non_ter]+=get_First(add_non_ter)
    for i in f.keys():
        f[i] = list(set(f[i]))
    return f

def getFollow(ter):
    return generate_Follow()[ter]

def generate_First():
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = [LLProduct("E'->E")]
    for i in range(num):
        p = LLProduct(f.readline())
        products.append(p)

    sources = Lgenerate_First(products)
    for k in sources.keys():
        sources[k] = list(sources[k].first)
    return sources

def get_First(ter):
    f = generate_First()
    return f[ter]