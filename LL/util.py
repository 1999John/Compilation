"""
E->TE'
E'->+TE'|~
T->FT'
T'->*FT'|~
F->(E)|id
"""
from .first_follow_class import FF
from .products import Product
import re

sources = {}
products = []
ter = {'id':0,'+':1,'*':2,'(':3,')':4,'$':5}
non_ter = {'E':0,"E'":1,"T":2,"T'":3,"F":4}
def getFirst(products):
    sources = {}
    for i in range(len(products)):
        source = products[i].source
        if products[i].source not in sources.keys():
            sources[source] = FF(source)
        # 右边第一个是终结符直接加入
        # todo: 正则表达式1
        # "select|from|where|=|insert into|values|id|create|table|[+*A-Za-z~|][']?|[(),;]"
        if re.match("select|from|where|=|insert into|values|id|table|create|[,();]|~", products[i].right[0]):
            sources[source].first.append(products[i].right[0])
        # 右边第一个是非终结符，加入add集
        elif re.match("[A-Z]'?", products[i].right[0]):
            sources[source].add.append(products[i].right[0])

        # 寻找产生式的或， 重复上述步骤
        try:
            # todo: 正则表达式2
            # todo: LR.__init__.py 正则表达式
            if re.match("select|from|where|=|insert into|values|id|table|create|[,();]|~", products[i].right[products[i].right.index('|') + 1]):
                sources[source].first.append(products[i].right[products[i].right.index('|') + 1])
            elif re.match("[A-Z]'?", products[i].right[products[i].right.index('|') + 1]):
                sources[source].add.append(products[i].right[products[i].right.index('|') + 1])
        except:
            continue

    for i in range(len(sources)):
        for s in sources.keys():
            if len(sources[s].add) > 0:
                for s_add in sources[s].add:
                    sources[s].first += sources[s_add].first
    for s in sources.keys():
        sources[s].first = set(sources[s].first)
        sources[s].reset_add()
    return sources
"""
E->TE'
E'->+TE'|~
T->FT'
T'->*FT'|~
F->(E)|id
"""
def getFollow():
    # todo
    sources["E"].follow = ['$',')']
    sources["E'"].follow = ['$',')']
    sources["T"].follow = ['+','$',')']
    sources["T'"].follow = ['+','$',')']
    sources["F"].follow = ['*','+','$',')']


analysis_table = []
def get_analysis_table():
    ret = [[0 for _ in range(6)] for i in range(5)]
    ret[0][0] = ['T',"E'"]
    ret[0][3] = ['T',"E'"]
    ret[1][1] = ['+','T',"E'"]
    ret[1][4] = ['~']
    ret[1][5] = ['~']
    ret[2][0] = ['F',"T'"]
    ret[2][-3] = ['F',"T'"]
    ret[3][1] = ['~']
    ret[3][2] = ['*','F',"T'"]
    ret[3][4] = ['~']
    ret[3][-1] = ['~']
    ret[4][0] = ['id']
    ret[4][3] =['(','E',')']
    return ret

def parse_string_to_pds(s) -> list:
    for i in s:
        p = Product(i)
        products.append(p)
def parse_inp(inp)->list:
    return re.findall("id|[()a-z*+]",inp)

if __name__ == '__main__':
    # s = ["E->TE'",
    #      "E'->+TE'|~",
    #      "T->FT'",
    #      "T'->*FT'|~",
    #      "F->(E)|id"]
    # parse_string_to_pds(s)
    # getFirst()
    # getFollow()
    analysis_table = get_analysis_table()
    st = ['$','E']
    inp = parse_inp(input())
    inp.append("$")
    ip = 0
    X = st[-1]
    while X!='$':
        if X==inp[ip]:
            st.pop(-1)
            ip+=1
        elif re.match("id|[a-z+*()~]",X):
            print("弹栈，弹出非终结符{}".format(X))
            if X == ')':
                print("括号不匹配")
            exit(0)
        elif analysis_table[non_ter[X]][ter[inp[ip]]]==0:
            print("输入串跳过记号{}，用户多输入了一个{}".format(inp[ip],inp[ip]))
            exit(0)
        elif analysis_table[non_ter[X]][ter[inp[ip]]]!=0:
            print(X,'->',analysis_table[non_ter[X]][ter[inp[ip]]])
            st.pop(-1)
            for f in range(len(analysis_table[non_ter[X]][ter[inp[ip]]])-1,-1,-1):
                if analysis_table[non_ter[X]][ter[inp[ip]]][f]=='~':
                    continue
                st.append(analysis_table[non_ter[X]][ter[inp[ip]]][f])
        X = st[-1]
    print("0 error 0 warning")

