import os

path = "./matrixes/"
pathout = "./outputs/"

i = 0
lim = 468
smells = ['CG', 'ROC', 'NC', 'LC', 'IM', 'IdQ', 'IQ', 'AQ', 'LPQ']

while(i <= lim):
    for metric in smells:
        os.system("qsmell -s " + metric + " -i " + path + "mat" + str(i) + ".csv -o " + pathout + "mat" + metric + str(i) + ".csv")
    i = i+1
        
    