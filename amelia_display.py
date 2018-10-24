from anytree import Node, RenderTree
from os import system
import amelia_dp

class displayTree():

    def __init__(self,nodeList):
        self.nodeList=nodeList

    def treeToPic(self,pictureName):
        dpList=amelia_dp.computeDpPoints(self.nodeList)
        text='digraph tree {'
        for i in range(len(self.nodeList)):
            text+='    \"'+str(self.nodeList[i])+'\" [label=\"'+  self.nodeList[i].name+"\ndp="+str(dpList[i])+"\"];"
        for i in range(1,len(self.nodeList)):
            text+='    \"'+ str(self.nodeList[i].parent)+'\" ->\"'+ str(self.nodeList[i]) + "\";"
        text+="}"
        self.writeDOTFile(pictureName, text.replace("ʌ",'\u028C'))
        self.convertDOTToPNG(pictureName)

    def writeDOTFile(self,filename, textToSave):
        textFile=open('graph.txt','wb')
        textFile.write(textToSave.encode('utf8'))
        textFile.close()

    def convertDOTToPNG(self,pictureName):
        system("dot graph.txt -T png -o "+pictureName)

    def drawTree(self):
        return self.nodeList, iter(amelia_dp.computeDpPoints(self.nodeList))

    def drawTreeInCMD(self):
        for pre, _, node in RenderTree(self.nodeList[0]):
            print("%s%s" % (pre, node.name))

    def drawTreeInCMDWithDp(self):
        dpListIterator=iter(amelia_dp.computeDpPoints(self.nodeList))
        for pre, _, node in RenderTree(self.nodeList[0]):
            print("%s%s dp=%g" % (pre, node.name, next(dpListIterator)))
