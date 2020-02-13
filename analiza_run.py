import amelia, amelia_dp, amelia_display
from amelia_prepare_file import *

def compute_dfMeasures(formula_raw, formula_raw_neg):
    if len(formula_raw)==1 or len(formula_raw)==2 and formula_raw[0]=='~':
        if len(formula_raw)==1:
            dfMeasures=[[formula_raw,1,0.5,0.5,1,1,0,1,0]]
        elif len(formula_raw)==2:
            dfMeasures=[[formula_raw[1:],1,0.5,0.5,1,0,1,0,1]]
    elif len(formula_raw)>2:
        formula=prepare_tree(formula_raw)
        formula_neg=prepare_tree(formula_raw_neg)
        dfMeasures=amelia_dp.measures(formula,formula_neg)
    return prepare_NaN_data(dfMeasures)

first=True
last=""
with open('up_to_6.txt') as infile:
    with open("out.txt", "w") as outfile:
        for indx, line in enumerate(infile):
            if first:
                data_to_file=prepare_header(line)
                first=False
                outfile.write("%s\n" % data_to_file)
            else:
                if not line==";;;;;;;;;" and not line=="":
                    formula_raw=line[0:line.find(",")]
                    if not formula_raw==last:
                        last=formula_raw
                        formula_raw=change_conj(formula_raw)
                        formula_raw=remove_parenthesis(formula_raw)
                        formula_raw_neg="~("+formula_raw+")"
                        formula_raw_neg=remove_parenthesis(formula_raw_neg)
                        dfMeasures=compute_dfMeasures(formula_raw, formula_raw_neg)
                        #print("\nrezultat:",formula_raw,indx, dfMeasures,"\n****")
                        #data_to_file=line.rstrip()+","+dfMeasures
                        data_to_file=last+","+dfMeasures
                        outfile.write("%s\n" % data_to_file)
            if indx%1000==0:
                print(indx)
