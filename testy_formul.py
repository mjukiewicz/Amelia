import amelia, amelia_dp, amelia_display
import amelia_prepare_file

def prepare_tree(input_data):
    formula=amelia.formationTree(input_data)
    formula=amelia_prepare_file.remove_parenthesis(formula)
    tree=amelia_display.displayTree(formula.giveMeTree())
    tree.drawTreeInCMDWithDp()
    return formula

#lista=['((~p=q)->p)=~(r->q)','~(p=q)->~(p=(r->~q))','p=~((q->p)=(~r->q))','~(p=(q->p))=(r->q)','~((p=q)->(p=r))->q','~((p=q)->(p=(r->q)))']
lista=["~(p=q) & (p -> r)", "(p=q) & ~(p -> r)", "~(~(p=q) & (p -> r))", "~((p=q) & ~(p -> r))", "~(~(~(p=q) & (p -> r)))", "~(~(~(p=q) & ~p) -> r)", "~(~(~((p=q) & (p -> r))))", "~(~(~(~p=q) & ~p) -> r)", "~(~(~((~p=q) & (p -> r))))", "~(~(~(p v q) -> (p & r)))", "~(~(~(p v q) -> ~p) & r)", "~(~(~((p v q) -> (p & r))))"]
lista=["~(~(~((p=q) & (p -> r))))", "~(~(~((~p=q) & (p -> r))))", "~(~(~((p v q) -> (p & r))))"]


for i in range(len(lista)):
    formula_raw=amelia_prepare_file.change_conj(lista[i])
    formula_raw_neg="~("+formula_raw+")"
    #formula=prepare_tree(formula_raw)
    formula_neg=prepare_tree(formula_raw_neg)
    #dfMeasures=amelia_dp.measures(formula,formula_neg)
    #print("\nrezultat:",i, dfMeasures,"\n****")
