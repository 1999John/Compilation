from .product import Product
from .project import Project
from .util import *
import numpy as np
from . import *
from .Follow_First import getFollow
def build_DFA(queue):
    count = 0
    while len(queue) != 0:
        project = queue.pop(0)
        ori = len(Project.projects)
        for ele in project.get_ele_after_dot():
            p = project.goto(ele)
            queue.append(p)
        cur = len(Project.projects)
        if ori == cur:
            count += 1
            if count == 10:
                break
        else:
            ori = cur


def build_SLR(flag=None):
    action_di,goto_di = get_di()
    if flag is None:
        analysis_table = {0: {"action": [5, np.nan, np.nan, 4, np.nan, np.nan], "goto": [1, 2, 3]},
                          1: {"action": [np.nan, 6, np.nan, np.nan, np.nan, "acc"], "goto": [np.nan, np.nan, np.nan]},
                          2: {"action": [np.nan, -2, 7, np.nan, -2, -2], "goto": [np.nan, np.nan, np.nan]},
                          3: {"action": [np.nan, -4, -4, np.nan, -4, -4], "goto": [np.nan, np.nan, np.nan]},
                          4: {"action": [5, np.nan, np.nan, 4, np.nan, np.nan], "goto": [8, 2, 3]},
                          5: {"action": [np.nan, -6, -6, np.nan, -6, -6], "goto": [np.nan, np.nan, np.nan]},
                          6: {"action": [5, np.nan, np.nan, 4, np.nan, np.nan], "goto": [np.nan, 9, 3]},
                          7: {"action": [5, np.nan, np.nan, 4, np.nan, np.nan], "goto": [np.nan, np.nan, 10]},
                          8: {"action": [np.nan, 6, np.nan, np.nan, 11, np.nan], "goto": [np.nan, np.nan, np.nan]},
                          9: {"action": [np.nan, -1, 7, np.nan, -1, -1], "goto": [np.nan, np.nan, np.nan]},
                          10: {"action": [np.nan, -3, -3, np.nan, -3, -3], "goto": [np.nan, np.nan, np.nan]},
                          11: {"action": [np.nan, -5, -5, np.nan, -5, -5], "goto": [np.nan, np.nan, np.nan]}}
        return analysis_table
    else:
        analysis_table = {}
        for state, project in enumerate(Project.projects):
            analysis_table[state] = {"action": [np.nan for _ in range(len(action_di))], "goto": [np.nan for _ in range(len(goto_di))]}
            action_goto_list = project.get_ele_after_dot()
            for ter in action_goto_list:
                if re.match("[A-Z][']*", ter):
                    analysis_table[state]["goto"][get_goto_position(ter)] = Project.projects.index(project.goto(ter))
                else:
                    analysis_table[state]["action"][get_action_position(ter)] = Project.projects.index(
                        project.goto(ter))
            for p in project.products:
                dot = p.right.index("·")
                if dot + 1 == len(p.right):
                    p_ = p.copy()
                    p_.right = p_.right[:-1]
                    ind = get_ret_ind(p_)
                    for _ in getFollow(p_.left):
                        analysis_table[state]["action"][get_action_position(_)] = ind
        return analysis_table


if __name__ == '__main__':
    f = open("test.txt", 'r')
    num = int(f.readline())
    products = []
    for i in range(num):
        product = f.readline()
        product = Product(product)
        products.append(product)

    project = Project(products, True)
    build_DFA([project])
    an_1 = build_SLR(project)
    an_2 = build_SLR()
    print(an_1)
    print(an_2)