import pandas


pathO = "./outputs/"
path1 ="./matrixes/"
smells = ['CG', 'ROC', 'LC', 'IM', 'IdQ', 'IQ']

i = 0

with open("./results.txt", "w") as res:
    while(i <= 379):
        res.write("\n========================================================\n")
        with open(path1 + "circuit"+ str(i) + ".txt", "r") as name:
            res.write(name.read())
        
        f = pandas.read_csv(path + 'matCG' + str(i) + '.csv')
        if(f['value'][0] >= 1):
            res.write("CG smell is present\n")
        f = pandas.read_csv(path + 'matROC' + str(i) + '.csv')
        if(f['value'][0] >= 1):
            res.write("ROC smell is present\n")
        f = pandas.read_csv(path + 'matLC' + str(i) + '.csv')
        if(f['value'][0] >= 1):
            res.write("LC smell is present\n")
        

    
    
    
    
        if(i == 0):
            i = i + 2
        else:
            i = i + 1
    