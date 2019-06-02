import amelia, amelia_dp, amelia_display
import amelia_prepare_file

def prepare_tree(input_data):
    formula=amelia.formationTree(input_data)
    tree=amelia_display.displayTree(formula.giveMeTree())
    tree.drawTreeInCMDWithDp()
    return formula

lista=['((~p=q)->p)=~(r->q)','~(p=q)->~(p=(r->~q))','p=~((q->p)=(~r->q))','~(p=(q->p))=(r->q)','~((p=q)->(p=r))->q','~((p=q)->(p=(r->q)))']

for i in lista:
    formula_raw=amelia_prepare_file.change_conj(i)
    formula_raw_neg="~("+formula_raw+")"
    formula=prepare_tree(formula_raw)
    formula_neg=prepare_tree(formula_raw_neg)
    dfMeasures=amelia_dp.measures(formula,formula_neg)
    print("\nrezultat:",i, dfMeasures,"\n****")
