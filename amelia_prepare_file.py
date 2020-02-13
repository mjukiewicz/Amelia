import amelia, amelia_dp, amelia_display

def change_conj(formula):
    formula=formula.replace("p1","p").replace("p2","q").replace("p3","r").replace("p4","s").replace("p5","t")
    return formula.replace("->","→").replace("&","ʌ")

def remove_parenthesis(formula):
    formula_list=list(formula.replace(" ",""))
    for j in range(formula.count("(")):
        for i in range(len(formula_list)):
            if formula_list[i]=='(' and formula_list[i+2]==')':
                formula_list[i]=' '
                formula_list[i+2]=' '
            elif formula_list[i]=='(' and formula_list[i+3]==')':
                formula_list[i]=' '
                formula_list[i+3]=' '
        formula_list=list("".join(formula_list).replace(" ","").replace("~~",""))
    formula_str="".join(formula_list)
    formula_list = list(formula_str.replace(" ",""))
    return "".join(formula_list).replace(" ","")

def prepare_NaN_data(data):
    vars=['p','q','r','s','t']
    data_new=[[i,'-','-','-','-'] for i in vars]
    for j in vars:
        for i in range(len(data)):
            if j==data[i][0]:
                data_new[vars.index(j)]=data[i]
    data_out=[str(j) for i in data_new for j in i if not j in vars]
    return ",".join(data_out)

def prepare_tree(input_data):
    formula=amelia.formationTree(input_data)
    tree=amelia_display.displayTree(formula.giveMeTree())
    if check_tree_correctness(tree):
        tree.drawTreeInCMDWithDp()
        input()
    return formula

def check_tree_correctness(tree):
    leaves_list=tree.leaves()
    letters = ["p","q","r","s","t","~p","~q","~r","~s","~t"]
    for i in leaves_list:
        if not i.replace(" ","") in letters:
            return True
    return False

def prepare_header(first_line):
    header=first_line
    new_header=''
    for i in ['p','q','r','s','t']:
        for j in ['A','B','C','D']:
            new_header+=','+j+'('+i+')'
    return header.rstrip()+new_header
