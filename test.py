def implicationAndParenthesis(formula):
    for j in range(len(formula)):
        if formula[j]=="→" and any(char in formula[j-3:j-1] for char in ('ʌ','v')):
            leftParenthesis=formula.rfind("(",0,j)
            if not any(char in formula[leftParenthesis+1:j] for char in ('(',')')):
                formula=formula[:leftParenthesis+1]+'('+ formula[leftParenthesis+1:j]+')'+formula[j:]
        elif formula[j]=="→" and any(char in formula[j+2:j+3] for char in ('ʌ','v')):
            rightParenthesis=formula.find(")",j)
            if not any(char in formula[j:rightParenthesis] for char in ('(',')')):
                formula=formula[:j+1]+'('+ formula[j+1:rightParenthesis]+')'+formula[rightParenthesis:]
    import re
    for j in set("".join(re.findall("[a-zA-Z]+", formula))):
        formula=formula.replace("("+j+")",j)

    print(formula)


implicationAndParenthesis('(p→(s→r))→((svr)v(p→q))')
