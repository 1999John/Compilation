from flask import render_template
from flask import request
from flask import Flask
from LR.util import *
from LR.SLR import *
from DataStruct.MyList import MyList
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Tree
from bs4 import BeautifulSoup

app = Flask(__name__)
action_di, goto_di = get_di()
ori_project = get_ori_project()
build_project = Project(ori_project.products, True)
build_DFA([build_project])
analysis_table = build_SLR(True)
context = {'action_di': action_di,
           'goto_di': goto_di,
           'analysis_table': analysis_table}


@app.route('/')
def hello_world():
    return render_template("index.html", **context)


@app.route('/compile', methods=['POST'])
def compile():
    inp = request.form['code']
    print(inp)
    try:
        inp = parse_inp(inp, context)
    except Exception as e:
        return render_template("index.html", **context)
    print(inp)
    stack = [0]
    try:
        while True:
            cur_state = stack[-1]
            ter = inp[0]
            ind = get_action_position(ter)
            cont = analysis_table[cur_state]["action"][ind]
            if cont is np.nan:
                print("error")
                context["error"] = "error"
                return render_template("index.html", **context)
            elif cont == "acc":

                context['answer'] = stack[-2].val
                if type(context['answer']) == type(pd.DataFrame()):
                    context['answer'] = context['answer'].to_html()
                if type(context['answer']) == type(pd.Series()):
                    html = """<table border="1"><tr><th>{}</th></tr>""".format(context['answer'].name)
                    for i in context['answer'].items():
                        html += "<tr><th>{}<th><tr>".format(i[-1])
                    html += "</table>"
                    context['answer'] = html
                print(stack[-2].val)
                print("0 error,0 warning")
                context['error'] = "0 error,0 warning"
                c = (
                    Tree()
                        .add("", [stack[-2].posi])
                        .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
                        .render("tree_base.html")
                )
                html = open("tree_base.html").read()
                soup = BeautifulSoup(html)
                gtree = str(soup.find("body"))[6:-7]
                context['tree'] = gtree
                return render_template("index.html", **context)
            elif cont >= 0:
                print("移进")
                inp = inp[1:]
                stack.append(ter)
                stack.append(cont)
                ter = inp[0]
                cur_state = stack[-1]
            elif cont < 0:
                cont = 0 - cont - 1
                p = ori_project.products[cont]
                print("按照" + str(p) + "规约")
                poplist = MyList()
                for _ in range((len(p.right) - 1) * 2):
                    poplist.append(stack.pop())
                non_ter = compute(p, poplist, context)
                cur_state = stack[-1]
                stack.append(non_ter)
                goto_ind = get_goto_position(p.left)
                goto_state = analysis_table[cur_state]["goto"][goto_ind]
                if goto_state is np.nan:
                    print("error")
                    context["error"] = "error"
                    return render_template("index.html", **context)
                else:
                    stack.append(goto_state)
                    cur_state = goto_state
        return render_template("index.html", **context)
    except Exception as e:
        return render_template("index.html", **context)


if __name__ == '__main__':
    app.run(debug=True)
