from tkinter import *
import amelia, amelia_dp, amelia_display
from anytree import Node, RenderTree
from PIL import Image , ImageTk

class AmeliaGUI (Frame , object ):
    def __init__(self, master):
        super(AmeliaGUI , self).__init__(master)
        self.master.title("Amelia GUI")
        glowneOkno.geometry("1350x650")
        #glowneOkno.state('zoomed')
        glowneOkno.resizable(0,0)
        self.pack(fill =BOTH , expand =1)
        self.stworzWidgety()

    def stworzWidgety(self):
        buttonWidth=17
        smallButtonWidth=5
        shift=200
        przyciskSprawdzenie = Button(self, text = "Check formula", width=buttonWidth, command=self.checkFormula)
        przyciskSprawdzenie.place(x=850+shift, y=170)
        self.przyciskDrzewo = Button(self, text = "Generate tree", width=buttonWidth, state=DISABLED, command=lambda:self.generateTree(0))
        self.przyciskDrzewo.place(x=700+shift, y=170)
        self.przyciskDrzewoDF = Button(self, text = "Generate tree with df", width=buttonWidth, state=DISABLED, command=lambda:self.generateTree(1))
        self.przyciskDrzewoDF.place(x=700+shift, y=220)
        self.przyciskDrzewoOblDF = Button(self, text = "Compute df", width=buttonWidth, state=DISABLED, command=self.comupteDp)
        self.przyciskDrzewoOblDF.place(x=850+shift, y=220)
        self.przyciskDrzewoPic = Button(self, text = "Generate tree in PNG", width=buttonWidth, state=DISABLED, command=self.generateTreePNG)
        self.przyciskDrzewoPic.place(x=700+shift, y=270)
        self.przyciskDrzewoPrev = Button(self, text = "PNG preview", width=buttonWidth, state=DISABLED, command=self.imagePreview)
        self.przyciskDrzewoPrev.place(x=850+shift, y=270)
        przyciskImplikacja = Button(self, text = "→", width=smallButtonWidth, command=self.insertImplication)
        przyciskImplikacja.place(x=700+shift, y=130)
        przyciskAlternatywa = Button(self, text = "v", width=smallButtonWidth, command=self.insertOR)
        przyciskAlternatywa.place(x=770+shift, y=130)
        przyciskKoniunkcja = Button(self, text = "ʌ", width=smallButtonWidth, command=self.insertAND)
        przyciskKoniunkcja.place(x=840+shift, y=130)
        przyciskNegacja = Button(self, text = "~", width=smallButtonWidth, command=self.insertNOT)
        przyciskNegacja.place(x=910+shift, y=130)
        opisPolaTekstowego=Label(self,text="Formula:")
        opisPolaTekstowego.place(x=700+shift, y=70)
        self.oldText=StringVar()
        self.oldText.trace("w", self.textChanged)
        self.oldText.set("pvq→r")
        self.poleTekstowe = Entry (self, width=50,textvariable=self.oldText)
        self.poleTekstowe.place(x=700+shift, y=100)
        self.tekst=Text(self, height=37, width=105)
        self.tekst.place(x=0, y=0)
        #self.poleTekstowe.insert(END, "pvq→r")
        self.tekstDF=Text(self, height=10, width=35)
        self.tekstDF.place(x=700+shift, y=325)
        scrollbar = Scrollbar(self.tekst)
        scrollbar.place(x=625+shift, height=595)
        scrollbar.config(command=self.tekst.yview)
        self.tekst.config(yscrollcommand=scrollbar.set)

    def textChanged(self,*args):
        self.przyciskDrzewo.config(state="disabled")
        self.przyciskDrzewoDF.config(state="disabled")
        self.przyciskDrzewoOblDF.config(state="disabled")
        self.przyciskDrzewoPic.config(state="disabled")
        self.przyciskDrzewoPrev.config(state="disabled")

    def checkFormula(self):
        if not amelia.formationTree.checkFormulaCorrectness(self,self.poleTekstowe.get()):
            self.przyciskDrzewo.config(state="normal")
            self.przyciskDrzewoDF.config(state="normal")
            self.przyciskDrzewoOblDF.config(state="normal")
            self.przyciskDrzewoPic.config(state="normal")
            self.przyciskDrzewoPrev.config(state="normal")

    def insertImplication(self):
        self.poleTekstowe.insert(self.poleTekstowe.index(INSERT),"→")

    def insertOR(self):
        self.poleTekstowe.insert(self.poleTekstowe.index(INSERT),"v")

    def insertAND(self):
        self.poleTekstowe.insert(self.poleTekstowe.index(INSERT),"ʌ")

    def insertNOT(self):
        self.poleTekstowe.insert(self.poleTekstowe.index(INSERT),"~")

    def generateSingleTree(self, tree, mode):
        nodeList, dfIterator=tree.drawTree()
        if mode==0:
            for pre, _, node in RenderTree(nodeList[0]):
                self.tekst.insert(END, "%s%s\n" % (pre, node.name))
        elif mode==1:
            for pre, _, node in RenderTree(nodeList[0]):
                self.tekst.insert(END, "%s%s df=%g\n" % (pre, node.name, next(dfIterator)))

    def generateTree(self, mode):
        self.tekst.delete('1.0', END)
        formula1=amelia.formationTree(self.poleTekstowe.get())
        tree1=amelia_display.displayTree(formula1.giveMeTree())
        self.generateSingleTree(tree1,mode)
        self.tekst.insert(END, "\n\n")
        formula2=self.checkIfNegation(self.poleTekstowe.get())
        tree2=amelia_display.displayTree(formula2.giveMeTree())
        self.generateSingleTree(tree2,mode)

    def checkIfNegation(self, formula):
        if formula[0]=="~":
            if formula.count('ʌ')+formula.count('v')+formula.count('→')==formula.count('('):
                formula2=amelia.formationTree(formula[1:])
            else:
                formula2=amelia.formationTree(formula[2:-1])
        else:
            if formula.count('ʌ')+formula.count('v')+formula.count('→')==formula.count('('):
                formula2=amelia.formationTree("~"+formula)
            else:
                formula2=amelia.formationTree("~("+formula+")")
        return formula2

    def generateTreePNG(self):
        formula1=amelia.formationTree(self.poleTekstowe.get())
        tree1=amelia_display.displayTree(formula1.giveMeTree())
        tree1.treeToPic('tree1.png')
        formula2=self.checkIfNegation(self.poleTekstowe.get())
        tree2=amelia_display.displayTree(formula2.giveMeTree())
        tree2.treeToPic('tree2.png')

    def imagePreview(self):
        obrazekOkno1=Toplevel()
        obrazekOkno1.title("Base formula")
        obrazTk = ImageTk.PhotoImage(file='tree1.png')
        label = Label(obrazekOkno1, image=obrazTk)
        label.image = obrazTk
        label.pack()
        obrazekOkno2=Toplevel()
        obrazekOkno2.title("Formula with negation")
        obrazTk = ImageTk.PhotoImage(file='tree2.png')
        label = Label(obrazekOkno2, image=obrazTk)
        label.image = obrazTk
        label.pack()

    def comupteDp(self):
        self.tekstDF.delete('1.0', END)
        formula1=amelia.formationTree(self.poleTekstowe.get())
        formula2=self.checkIfNegation(self.poleTekstowe.get())
        dfMeasures=amelia_dp.measures(formula1,formula2)
        for variableResults in dfMeasures:
            for j in range(len(variableResults)):
                if j==0:
                    self.tekstDF.insert(END, variableResults[j])
                else:
                    self.tekstDF.insert(END, " %.2f" %(float(variableResults[j])))
            self.tekstDF.insert(END, '\n')

glowneOkno = Tk()
app = AmeliaGUI(glowneOkno)
app.textChanged()
glowneOkno.mainloop()
