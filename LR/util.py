import re
from .product import Product
from .project import Project
from . import *
def parse_inp(inp):
    ret = re.findall("id|[+*A-Za-z~|][']?|[()]|·", inp)
    ret.append("$")
    return ret

def get_action_position(id):
    return action_di[id]

def get_goto_position(non_ter):
    return goto_di[non_ter]

def get_ori_project():
    f = open("LR/test.txt","r")
    num = int(f.readline())
    products = []
    for i in range(num):
        p = Product(f.readline())
        products.append(p)
    return Project(products)

def get_ret_ind(product):
    if product.left=="E'":
        return "acc"
    ori = get_ori_project()
    return 0-ori.products.index(product)-1