import amelia, amelia_display
import statistics
from anytree import Node, RenderTree

def extractVariables(formula):
    setOfVariables=set([i for i in formula if i.isalpha()])
    setOfVariables.discard('ʌ')
    setOfVariables.discard('v')
    return sorted(setOfVariables)

def measures(formula1, formula2):
    variables=extractVariables(formula1.formulaWithCorrectSpaces)
    dpValues=[[] for i in range(0, len(variables))]
    for j in range(len(variables)):
        dpValues[j]=createListOfDpValues(listOfDpValues(formula1), variables[j], dpValues[j])
        dpValues[j]=createListOfDpValues(listOfDpValues(formula2), variables[j], dpValues[j])

    results=[]
    for i in range(len(dpValues)):
        values=[j[1] for j in dpValues[i]]
        valuesNeg=[j[1] for j in dpValues[i] if j[0][0]=='~']
        valuesWithoutNeg=[j[1] for j in dpValues[i] if not j[0][0]=='~']
        if valuesNeg==[]:
            measureD=max(valuesWithoutNeg)
        elif valuesWithoutNeg==[]:
            measureD=max(valuesNeg)
        else:
            #print(dpValues,values, valuesNeg, valuesWithoutNeg)
            measureD=(max(valuesNeg)+max(valuesWithoutNeg))/2

        scoreNP=1
        for x in valuesNeg:
            scoreNP*=x
        scoreP=1
        for x in valuesWithoutNeg:
            scoreP*=x

        scoreNS=sum([i for i in valuesNeg])
        scoreS=sum([i for i in valuesWithoutNeg])

        results.append([variables[i],max(values),statistics.mean(values),statistics.median(values), measureD, scoreS, scoreNS, scoreP, scoreNP])

    return results

def createListOfDpValues(formula, variable, dpValues):
    dpValues.extend([i for i in formula if variable in i[0]])
    varsUsed=[k[0] for k in formula]
    # if not variable in varsUsed:           #zakomentowac jesli wersja bez zer
    #     dpValues.append([variable,0])      #
    # elif not "~"+variable in varsUsed:     #
    #     dpValues.append(["~"+variable,0])  #
    return dpValues

def listOfDpValues(formula):
    nodeList=formula.giveMeTree()
    tree=amelia_display.displayTree(nodeList)
    dpValues=[]
    dpListIterator=iter(computeDpPoints(nodeList))
    for pre, _, node in RenderTree(nodeList[0]):
        value=next(dpListIterator)
        if len(node.name)<=3:
            dpValues.append([node.name.replace(" ",""), value])
    return dpValues

def checkIfNegation(formula):
    n_par=formula.count("(")
    n_conj=formula.count("→")+formula.count("ʌ")+formula.count("v")+formula.count("=")
    if formula[0]=='~' and formula[1]=='(' and formula[-1]==')' and n_conj<=n_par:
        negation=True
        formula=formula[2:-1]
    else:
        negation=False
    return negation, formula


def conjunctionFind(formula):
    spojniki=['v','ʌ','→','=']
    for j in range(len(formula)):
        if formula[:j].count("(")-formula[:j].count(")")==0 or formula[j:].count("(")-formula[j:].count(")")==0:
            if formula[j] in spojniki:
                return formula[j]

def computeDpPoints(nodeList):
    dpList=[1]
    for i in range(1,len(nodeList)):
        negation, formulaParent=checkIfNegation(nodeList[i].parent.name)
        parentConjunction=conjunctionFind(formulaParent)
        parentWartosc=dpList[nodeList.index(nodeList[i].parent)]
        if parentConjunction== 'ʌ' and negation:
            dpList.append(parentWartosc*1)
        elif parentConjunction == "=" and negation:
            dpList.append(parentWartosc*1)
        elif parentConjunction== 'v' and negation or parentConjunction== '→' and negation:
            dpList.append(parentWartosc*0.5)
        elif parentConjunction== '→' or parentConjunction== 'v':
            dpList.append(parentWartosc*1)
        elif parentConjunction== 'ʌ':
            dpList.append(parentWartosc*0.5)
        elif parentConjunction == "=":
            dpList.append(parentWartosc*0.5)
    return dpList
