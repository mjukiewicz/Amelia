import amelia, amelia_dp, amelia_display
import amelia_prepare_file

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
    tree.drawTreeInCMDWithDp()
    return formula
'''
with open('up_to_6.txt') as f:
    data_raw = f.read().splitlines()

header=data_raw[0]
new_header=''
for i in ['p','q','r','s','t']:
    for j in ['A','B','C','D']:
        new_header+=','+j+'('+i+')'
data_to_file=[header+new_header]
data_raw.pop(0)
formulas_list, raw_lines=[], []
for i in data_raw:
    if not i==";;;;;;;;;" and not i=="":
        formula_raw=i[0:i.find(",")]
        formulas_list.append(formula_raw)
        raw_lines.append(i)
'''
formulas_list=["~(p=q) & (p -> r)", "(p=q) & ~(p -> r)", "~(~(p=q) & (p -> r))", "~((p=q) & ~(p -> r))", "~(~(~(p=q) & (p -> r)))", "~(~(~(p=q) & ~p) -> r)", "~(~(~((p=q) & (p -> r))))", "~(~(~(~p=q) & ~p) -> r)", "~(~(~((~p=q) & (p -> r))))", "~(~(~(p v q) -> (p & r)))", "~(~(~(p v q) -> ~p) & r)", "~(~(~((p v q) -> (p & r))))"]
for i in range(len(formulas_list)):
    #i=17644
    formula_raw=amelia_prepare_file.change_conj(formulas_list[i])
    formula_raw=amelia_prepare_file.remove_parenthesis(formula_raw)
    formula_raw_neg="~("+formula_raw+")"
    formula_raw_neg=amelia_prepare_file.remove_parenthesis(formula_raw_neg)
    if len(formula_raw)==1 or len(formula_raw)==2 and formula_raw[0]=='~':
        if len(formula_raw)==1:
            dfMeasures=[[formula_raw,1,0.5,0.5,1]]
        elif len(formula_raw)==2:
            dfMeasures=[[formula_raw[1:],1,0.5,0.5,1]]
    elif len(formula_raw)>2:
        formula=prepare_tree(formula_raw)
        formula_neg=prepare_tree(formula_raw_neg)
        dfMeasures=amelia_dp.measures(formula,formula_neg)
    dfMeasures=prepare_NaN_data(dfMeasures)
    print("\nrezultat:",formulas_list[i],i, dfMeasures,"\n****")
    #data_to_file.append(raw_lines[i]+","+dfMeasures)

with open('up_to_6_większy.csv', 'w') as f:
    for item in data_to_file:
        f.write("%s\n" % item)
