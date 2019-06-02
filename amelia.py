from anytree import Node
from re import findall

formula1='(p → q) → ((p → r) → (p → (q ʌ r)))'
formula2='(((p v q) -> r) v s )-> ((s ʌ r) -> (p ->q))'
formula3='((p v q) ʌ ((p ʌ r) →q)) -> ((r → s) → ((q v p) ʌ ((r v s) →t)))'
formula4='~((p → q) → ((p → r) → (p → (q ʌ r))))'
formula5='~((((p v q) -> r) v s )-> ((s ʌ r) -> (p ->q)))'
formula6='~(((p v q) ʌ ((p ʌ r) →q)) -> ((r → s) → ((q v p) ʌ ((r v s) →t))))'

class formationTree():

    def __init__(self, baseFormula):
        #self.checkFormulaCorrectness(baseFormula)
        formulaWithCorrectParenthesis=self.implicationAndParenthesis(baseFormula)
        self.formulaWithCorrectSpaces=self.spacesInFormula(formulaWithCorrectParenthesis)
        self.formulaWithCorrectSpaces=self.removeDoubleNegation(self.formulaWithCorrectSpaces)
        self.nodeList= [Node(self.formulaWithCorrectSpaces)]
        self.treeExtraction(self.formulaWithCorrectSpaces, self.nodeList, self.nodeList[0])

    def checkFormulaCorrectness(self,formula):
        spojniki=['ʌ','v','→','=']
        decision=False
        formula="".join(formula.split())
        for j in range(1,len(formula)):
            if formula[j]==formula[j-1] and formula[j]!='(' and formula[j]!=')':
                decision=True
            if formula[j] in spojniki and formula[j-1] in spojniki:
                decision=True
            if formula.count("(")!=formula.count(")"):
                decision=True
        if sum([1 for i in formula if i.isalpha() and i!='v']) <= sum([1 for i in formula if i in spojniki]):
            decision=True
        return decision #czemu to nie jest uzywane?

    def implicationAndParenthesis(self,formula):
        for j in range(len(formula)):
            if formula[j]=="→" and any(char in formula[j-3:j-1] for char in ('ʌ','v')):
                leftParenthesis=formula.rfind("(",0,j)
                if not any(char in formula[leftParenthesis+1:j] for char in ('(',')')):
                    formula=formula[:leftParenthesis+1]+'('+ formula[leftParenthesis+1:j]+')'+formula[j:]
            elif formula[j]=="→" and any(char in formula[j+2:j+3] for char in ('ʌ','v')):
                rightParenthesis=formula.find(")",j)
                if not any(char in formula[j:rightParenthesis] for char in ('(',')')):
                    formula=formula[:j+1]+'('+ formula[j+1:rightParenthesis]+')'+formula[rightParenthesis:]
        for j in set("".join(findall("[a-zA-Z]+", formula))):
            formula=formula.replace("("+j+")",j)
        return formula

    def spacesInFormula(self,formula):
        formula="".join(formula.split())
        newFormula=''
        for i in range(len(formula)):
            if formula[i] == 'ʌ' or formula[i] == 'v' or formula[i] == '→' or formula[i] == "=":
                newFormula += ' ' + formula[i] + ' '
            else:
                newFormula += formula[i]
        if formula.count('=')+formula.count('ʌ')+formula.count('v')+formula.count('→')<=formula.count('(') and not formula[0]=='~':
            newFormula=newFormula[1:-1]
        return newFormula
#-----------
    def removeParenthesis(self,data):
        if data.count("(")==0 and data.count(")")==0:
            data="("+data+")"
        for i in range(max(data.count("("),data.count(")"))):
            if data.endswith(')') and data.startswith('('):
                break
            elif not data.endswith(')'):
                data=data[:-1]
            elif not data.startswith('('):
                data=data[1:]
        return data

    def mySignFunction(self,number):
        if number == 1:
            number = 0
        else:
            number = 1
        return number

    def conjunctionRules(self,conjunction,subformula1,subformula2,negation):
        if len(subformula1) < 3:
            subformula1=subformula1.strip(' ')
        if len(subformula2) < 3:
            subformula2=subformula2.strip(' ')
        multiplier1=self.mySignFunction(len(subformula1))
        multiplier2=self.mySignFunction(len(subformula2))

        if conjunction == '→' and negation:
            subformula2 = "~" + "(" * multiplier2 + subformula2 + ")" * multiplier2
        elif conjunction == '→':
            subformula1 = "~" + "(" * multiplier1 + subformula1 + ")" * multiplier1
        elif conjunction == "=" and negation:
            temp2 = "~" + "(" * (multiplier2+1) + subformula2 + ")" * multiplier2 + " → " + "(" * multiplier1 + subformula1 + ")" * (multiplier1+1)
            temp1 = "~" + "(" * (multiplier1+1) + subformula1 + ")" * multiplier1 + " → " + "(" * multiplier2 + subformula2 + ")" * (multiplier2+1)
            subformula1=temp1
            subformula2=temp2
        elif conjunction == "=":
            temp2 = "(" * multiplier2 + subformula2 + ")" * multiplier2 + " → " + "(" * multiplier1 + subformula1 + ")" * multiplier1
            temp1 = "(" * multiplier1 + subformula1 + ")" * multiplier1 + " → " + "(" * multiplier2 + subformula2 + ")" * multiplier2
            subformula1=temp1
            subformula2=temp2
        elif negation:
            subformula2 = "~" + "(" * multiplier2 + subformula2 + ")" * multiplier2
            subformula1 = "~" + "(" * multiplier1 + subformula1 + ")" * multiplier1

        subformula1=self.removeDoubleNegation(subformula1)
        subformula2=self.removeDoubleNegation(subformula2)
        return subformula1, subformula2

    def removeDoubleNegation(self,formula):
        n_conj=sum([1 for i in formula if i in ["→","ʌ","v","="]])
        n_par=formula.count("(")
        if n_conj==0 and formula[0:3]=="~(~":
            formula=formula[3]
        elif n_conj<n_par and formula[0:3]=="~(~":
            formula=formula[4:-2]
        return formula

    def checkIfNegation(self,formula):
        n_par=formula.count("(")
        n_conj=formula.count("→")+formula.count("ʌ")+formula.count("v")+formula.count("=")
        if formula[0]=='~' and formula[1]=='(' and formula[-1]==')' and n_conj<=n_par:
            negation=True
            formula=formula[2:-1]
        else:
            negation=False
        return negation, formula

    def subFormulasExtraction(self,formula, i):
        if len(formula[1:i-1])>1:
            if formula[0:2]=="~("and formula[i-2]==')':
                subformula1=formula[:i-1]
            else:
                subformula1=self.removeParenthesis(formula[:i])[1:-1]
        else:
            if formula[0]=='~':
                subformula1="~"+formula[1]
            else:
                subformula1=formula[0]
        if len(formula[i+1:-1])>1:
            if formula[i+2:i+4]=='~(' and formula[-1]==')':
                subformula2=formula[i+2:]
            else:
                subformula2=self.removeParenthesis(formula[i+2:])[1:-1]
            #if formula[i+2]=='~':
            #    subformula2="~("+subformula2+")"
            #    print(subformula2)
        else:
            subformula2=formula[-1]
        subformula1=self.removeDoubleNegation(subformula1)
        subformula2=self.removeDoubleNegation(subformula2)
        return subformula1, subformula2

    def treeExtraction(self,formula,nodeList,parent):
        negation, formula = self.checkIfNegation(formula)
        for i in range(len(formula)):
            if formula[i]== '→' or formula[i]== 'v' or formula[i]=='ʌ' or formula[i]=='=':
                if formula.count("(")==0 and formula.count(")")==0 and not formula[i]=='=':
                    subformula1, subformula2 = self.conjunctionRules(formula[i], formula[:i], formula[i+2:], negation)
                    self.nodeList.append(Node(subformula1, parent=nodeList[-1]))
                    self.nodeList.append(Node(subformula2, parent=nodeList[-2]))
                elif formula[:i].count("(")-formula[:i].count(")")==0 or formula[i:].count("(")-formula[i:].count(")")==0:
                    subformula1, subformula2=self.subFormulasExtraction(formula, i)
                    subformula1, subformula2=self.conjunctionRules(formula[i],subformula1,subformula2,negation)
                    leaf1=Node(subformula1, parent=parent)
                    leaf2=Node(subformula2, parent=parent)
                    self.nodeList.append(leaf1)
                    self.treeExtraction(subformula1,nodeList,leaf1)
                    self.nodeList.append(leaf2)
                    self.treeExtraction(subformula2,nodeList,leaf2)
                    break

    def giveMeTree(self):
        return self.nodeList
