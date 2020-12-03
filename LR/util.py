import re
from .product import Product
from .project import Project
from . import *
from .Ter import *
import numpy as np
import pandas as pd
def get_di():
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = []
    for i in range(num):
        p = Product(f.readline())
        products.append(p)
    non_ter_list = list(set([p.left for p in products]))
    ter_list = []
    for p in products:
        for _ in p.right:
            ter_list.append(_)
    ter_list = list(set(ter_list))
    ter_list.append('$')
    for non_ter in non_ter_list:
        if non_ter in ter_list:
            ter_list.remove(non_ter)
    action_di = {}
    for v,k in enumerate(ter_list):
        action_di[k] = v
    goto_di = {}
    for v,k in enumerate(non_ter_list):
        goto_di[k] = v
    return action_di,goto_di
def parse_inp(inp:str,context:dict):
    # todo: 这里需要修改正则表达式
    # todo: LL.products的正则表达式
    if "create" in inp:
        ret = re.findall("create|table|[A-Za-z]+[0-9_]*|[()]|,", inp)
        flag = False
        first = 0
        for i in range(len(ret)):
            if not re.match("create|table|[(),]",ret[i]):
                ret[i] = Ter((ret[i]))
                if not flag:
                    first = i
                    flag=True
        for _ in range(ret.count('')):
            ret.remove('')
        ret.append("$")
        if not re.match("[A-Za-z]+[0-9_]*",ret[first].val):
            print("表名: {} 不对".format(ret[first].val))
            context['error'] = "表名: {} 不对".format(ret[first].val)
            raise Exception
        if ret[first+1]!='(':
            print("建表错误")
            context['error'] = '建表错误'
            raise Exception
        return ret
    elif "insert" in inp:
        ret = re.findall("'[A-Za-z0-9*+/~]*'|insert into|[A-Za-z]+|[(),]",inp)
        flag = False
        first = 0
        for i in range(len(ret)):
            if not re.match("insert into|values|[(),]",ret[i]):
                ret[i] = Ter((ret[i]))
                if not flag:
                    first=i
                    flag=True
        for _ in range(ret.count('')):
            ret.remove('')
        ret.append("$")
        if not re.match("[A-Za-z]+[0-9_]*",ret[first].val):
            print("语法错误{}".format(ret[first].val))
            context['error'] = "语法错误{}".format(ret[first].val)
            raise Exception
        if ret[first+1]!='values':
            print("语法错误")
            print(inp)
            context['error'] = '语法错误: '+inp
            raise Exception
        return ret
    elif "select" in inp:
        ret = re.findall("select|’[A-Za-z0-9]+‘|[A-Za-z0-9]+|from|where|=|;|[*]",inp)
        for i in range(len(ret)):
            if not re.match("select|from|where|=|,|;",ret[i]):
                ret[i]=Ter(ret[i])
        for _ in range(ret.count('')):
            ret.remove('')
        if "where" not in ret:
            try:
                ret.insert(ret.index(';'),'~')
            except Exception as e:
                print("缺少终结符")
                context['error'] = '缺少终结符'
                raise Exception
        ret.append('$')
        return ret
    else:
        print("不支持:",inp)
        context['error']='语句出错: '+inp
        raise Exception

def get_action_position(id):
    action_di,_ = get_di()
    return action_di[str(id)]


def get_goto_position(non_ter):
    _,goto_di = get_di()
    return goto_di[non_ter]


def get_ori_project():
    f = open("LR/test.txt", "r")
    num = int(f.readline())
    products = []
    for i in range(num):
        p = Product(f.readline())
        products.append(p)
    return Project(products)


def get_ret_ind(product):
    if product.left == "E'":
        return "acc"
    ori = get_ori_project()
    return 0 - ori.products.index(product) - 1

"""
E->create table TF
F->(G)
G->G,G
G->id
T->id"""
def compute(p: Product, poplist: list,context:dict):
    root_dir = "db/"
    if str(p) == 'E->·createtableTF':
        E_ = NonTer('E')
        F = poplist.index('F')
        T = poplist.index('T')
        E_.val = pd.DataFrame(columns=F.val)
        E_.val.to_csv(root_dir+T.val+".csv",index=False)
        E_.posi = {"children":[{"name":"create"},{"name":"table"},T.posi,F.posi],"name":"E"}
        return E_
    elif str(p) == 'F->·(G)':
        F = NonTer('F')
        G = poplist.index('G')
        F.val = G.val
        F.posi = {"children":[{"name":")"},G.posi,{"name":")"}],"name":F}
        return F
    elif str(p) == 'G->·G,G':
        G_ = NonTer('G')
        G1 = poplist.index('G')
        G2 = poplist.index('G')
        G_.val = []
        if type(G1.val)==type([]):
            for i in G1.val:
                G_.val.append(i)
        else:
            G_.val.append(G1.val)
        if type(G2.val) == type([]):
            for i in G2.val:
                G_.val.append(i)
        else:
            G_.val.append(G2.val)
        if type(G1.val) ==type({}):
            G_.val = {}
            for k,v in G1.val.items():
                G_.val[k]=v
            for k,v in G2.val.items():
                G_.val[k]=v
        G_.posi = {"children":[G1.posi,{"name":","},G2.posi],"name":"G"}
        return G_
    elif str(p) == 'G->·id':
        G = NonTer('G')
        id_ = poplist.index('id')
        G.val = id_.val
        G.posi = {"children":[{"name":id_.val}],"name":"G"}
        return G
    elif str(p) == 'T->·id':
        T = NonTer('T')
        id_ = poplist.index('id')
        T.val = id_.val
        T.posi = {"children":[{"name":id_.val}],"name":"T"}
        return T
    elif str(p) =="E->·insert intoTvaluesF":
        F = poplist.index("F")
        T = poplist.index("T")
        try:
            df = pd.read_csv(root_dir+T.val+".csv",header=0,index_col=None)
        except Exception as e:
            print("表不存在")
            context['error']='表不存在'
            raise Exception
        di = {}
        for k,v in zip(df.columns,F.val):
            di[k] = v
        df = df.append(di,ignore_index=True)
        df.to_csv(root_dir+T.val+".csv",index=False)
        E = NonTer('E')
        E.val = df
        E.posi = {"children":[{"name":"insert into"},T.posi,{"name":"values"},F.posi],"name":"E"}
        return E
    elif str(p) =="H->·~":
        H = NonTer('H')
        H.val = True
        H.posi ={"children":[{"name":"~"}],"name":"H"}
        return H
    elif str(p) == 'G->·G=id':
        G_ = NonTer('G')
        G_.val ={}
        id_ = poplist.index('id')
        G = poplist.index('G')
        G_.val[G.val]=id_.val
        G_.posi = {"children":[G.posi,{"name":id_.val}],"name":"G"}
        return G_
    elif str(p) == 'H->·whereG':
        H = NonTer('H')
        G = poplist.index('G')
        H.val = G.val
        G.posi = {"children":[{"name":"where"},G.posi],"name":"G"}
        return H
    elif str(p) == "E->·selectGfromTH;":
        E = NonTer('E')
        H = poplist.index('H')
        T = poplist.index('T')
        G = poplist.index('G')
        try:
            T.val = pd.read_csv(root_dir + T.val + ".csv", header=0)
            E.posi = {"children":[{"name":"select"},G.posi,{"name":"from"},T.posi,H.posi],"name":"E"}
        except Exception as e:
            print("表不存在")
            context['error']='表不存在'
            raise Exception
        if H.val==True:
            flag = True
            if type(G.val)==type([]):
                for val in G.val:
                    if val not in T.val.columns.values:
                        flag = False
                        break
            else:
                if G.val not in T.val.columns.values:
                    flag = False
            if G.val=='*':
                E.val = T.val
            elif not flag:
                context['error'] = "列名不存在"
                raise Exception
            else:
                E.val = T.val[G.val]
            return E
        else:
            # todo: 暂时只能用等号
            for k,v in H.val.items():
                continue
            print(k,v)
            if G.val=='*':
                E.val = T.val[T.val[k]==str(v)]
            else:
                E.val = T.val[T.val[k]==str(v)][G.val]
            return E
    print(str(p))
    context['error']='产生式不存在'
    raise Exception