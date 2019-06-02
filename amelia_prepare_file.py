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

    for j in range(formula.count("(")):
        for i in range(len(formula_list)):
            if "".join(formula_list[i:i+4])=='~(~(' and "".join(formula_list[-2:])=='))':
                formula_list[i:i+4]='    '
                formula_list[-2:]='  '
        formula_list=list("".join(formula_list).replace(" ","").replace("~~",""))
    formula_str="".join(formula_list)

    for i in range(len(formula_str)):
        if formula_str[i] in ["→","ʌ","v","="] and formula_str[:i].count("(")-formula_str[:i].count(")")==0 and formula_str[i+1:].count("(")-formula_str[i+1:].count(")")==0:
            if formula_str[0]=='(' and formula_str[i-1]==')' and formula_str[:i].count("(")>1:
                formula_list[0]=' '
                formula_list[i-1]=' '
            if formula_str[i+1]=='(' and formula_str[-1]==')' and formula_str[i+1:].count(")")>1:
                formula_list[i+1]=' '
                formula_list[-1]=' '

    return "".join(formula_list).replace(" ","")
