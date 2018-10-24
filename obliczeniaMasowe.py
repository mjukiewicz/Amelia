import amelia, amelia_dp, amelia_display, amelia_LaN
import os
from sklearn.cross_decomposition import CCA
import numpy as np

def removeTrash(data):
    data=data.replace("`I`","→").replace("`A`","ʌ").replace("`D`","v")
    data=data.replace("N (V 1)","~p").replace("N (V 2)","~q").replace("N (V 3)","~r").replace("N (V 4)","~s")
    data=data.replace("V 1","p").replace("V 2","q").replace("V 3","r").replace("V 4","s")
    return data


filename="geo1.txt"
with open(filename, 'r') as inputFile:
    data = inputFile.read().splitlines(True)

resultsDP=[]
counter=1
oldCounter=-1
print(oldCounter)
n_components = 1
n_dp=4
resultsSorted=[]
for i in data:
    dane=removeTrash(i)
    tree1=amelia.formationTree(dane)
    tree2=amelia.formationTree("~("+dane+")")
    #treeToCmd=amelia_display.displayTree(tree1.giveMeTree())
    #treeToCmd.drawTreeInCMDWithDp()
    #treeToCmd=amelia_display.displayTree(tree2.giveMeTree())
    #treeToCmd.drawTreeInCMDWithDp()
    measures=amelia_dp.measures(tree1,tree2)
    resultsDP.append(measures)
    if int(100*counter/len(data))>oldCounter:
        oldCounter=int(100*counter/len(data))
        #os.system("cls")
        print(oldCounter)
    counter+=1
    n_var=len(amelia_dp.extractVariables(tree1.formulaWithCorrectSpaces))
    leafAndNodes=amelia_LaN.NodesAndLeafs(tree1.formulaWithCorrectSpaces)
    data2=[leafAndNodes.numberOfLeafs(),leafAndNodes.numberOfNodes()]
    data=[]
    for k in range(1,n_dp+1):
        for j in range(n_var):
            data.append(measures[j][k])

    data.extend(data2)
    resultsSorted.append(data)
resultsSorted=np.asarray(resultsSorted)
#print(resultsSorted)
cca = CCA(n_components)
d1=resultsSorted.T[:][:1].T
d2=resultsSorted.T[:][-2:].T
print(d1.shape,d2.shape)
cca.fit(d1, d2)
U, V = cca.transform(d1, d2)
print(abs(np.corrcoef(U.T, V.T)[0, 1]))


with open("dp_measures.txt", 'w') as outputFile:
    for line in resultsDP:
        outputFile.writelines(str(line)+"\n")
