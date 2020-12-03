from .product import Product
import re
def remove_same(products):
    ret = []
    for p in products:
        if p not in ret:
            ret.append(p)
    return ret

class Project:
    projects = []
    def __init__(self,products:list,initial=None):
        self.products = remove_same(products)
        if initial!=None:
            p = Product("E'->E")
            self.products.insert(0,p)
            for i in range(len(self.products)):
                self.products[i].right.insert(0,'·')
            Project.projects.append(self)
        self.points = []
    def goto(self,inp:str):
        ret_project = []
        for pro in self.products:
            p = pro.copy()
            dot = p.right.index('·')
            if dot+1 != len(p.right):
                if p.right[dot+1]==inp: # todo: 判断dot是否越界
                    inp_index = dot+1
                    p.right[dot],p.right[inp_index] = p.right[inp_index],p.right[dot]
                    ret_project.append(p)
                    ret_project += self._add_non_ter_product(p)

        rp = Project(ret_project)
        if rp not in Project.projects:
            Project.projects.append(rp)
        self.points.append(Project.projects[Project.projects.index(rp)])
        return Project.projects[Project.projects.index(rp)]
    def _add_non_ter_product(self,product):
        dot = product.right.index("·")
        ret = []
        if dot!=len(product.right)-1:
            if re.match("[A-Z][']*",product.right[dot+1]):
                for p in Project.projects[0].products:
                    if p.left==product.right[dot+1]:
                        ret.append(p)
        for i in range(len(Project.projects[0].products)):
            for p in ret[:]:
                dot_ = p.right.index("·")
                if re.match("[A-Z][']*",p.right[dot_+1]):
                    for p_ in Project.projects[0].products:
                        if p_.left==p.right[dot_+1] and p_ not in ret:
                            ret.append(p_)
        return ret

    def get_ele_after_dot(self):
        ret = []
        for p in self.products:
            dot = p.right.index("·")
            if len(p.right)!=dot+1:
                if p.right[dot+1] not in ret:
                    ret.append(p.right[dot+1])
        return ret

    def __eq__(self, o: object) -> bool:
        if len(self.products)!=len(o.products):
            return False
        for p in self.products:
            if p not in o.products:
                return False
        return True

    def __str__(self) -> str:
        ret = ""
        for p in self.products:
            ret+=str(p)+"\n"
        return ret