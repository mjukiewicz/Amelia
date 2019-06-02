def test_automatyczny(drzewo, formula,numer):
    print(formula)
    listaLiter=[i for i in formula if i.isalpha() and not i=="v" and not i=="ʌ"]
    for i in range(len(drzewo.nodeList[0].leaves)):
        if not str(drzewo.nodeList[0].leaves[i])[-3]:
            print("problem!",numer)


with open('up_to_6_większy.csv') as f1, open('up_to_6_większy_n.csv') as f2, open('outfile.txt', 'w') as outfile:
    i=0
    for line1, line2 in zip(f1, f2):
        if not line1 == line2:
            i+=1
            print(line1)
            print(line2)
            print(i,"-----")
