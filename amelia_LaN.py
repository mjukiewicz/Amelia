class NodesAndLeafs():

    def __init__(self, formula):
        self.forumla=formula

    def numberOfLeafs(self):
        return self.numberOfConj()+1

    def numberOfNodes(self):
        return self.numberOfConj()

    def numberOfConj(self):
        return self.forumla.count("→")+self.forumla.count("v")+self.forumla.count("ʌ")

'''
formula1='(p → q) → ((p → r) → (p → (q ʌ r)))'
formula2='(((p v q) → r) v s )→ ((s ʌ r) → (p →q))'
formula3='((p v q) ʌ ((p ʌ r) →q)) → ((r → s) → ((q v p) ʌ ((r v s) →t)))'

obiekt=NodesAndLeafs(formula1)
print(obiekt.numberOfLeafs(), obiekt.numberOfNodes())
obiekt=NodesAndLeafs(formula2)
print(obiekt.numberOfLeafs(), obiekt.numberOfNodes())
obiekt=NodesAndLeafs(formula3)
print(obiekt.numberOfLeafs(), obiekt.numberOfNodes())
'''
