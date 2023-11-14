import pandas
from statistics import *


path = "./outputs/"
smells = ['CG', 'ROC', 'LC', 'IM', 'IdQ', 'IQ']

for sm in smells:
    vet = []
    i = 0
    
    while(i <= 379):
        f = pandas.read_csv(path + 'mat' + sm + str(i) + '.csv')
        vet.append(int(f['value'][0]))
        if(i == 0):
            i = i + 2
        else:
            i = i + 1
    
    vet.sort()
    print("mean " + sm + ": " + str(mean(vet)))
    print("median " + sm + ": " + str(median(vet)))
    print("mode " + sm + ": " + str(mode(vet)))
    print("standard deviation " + sm + ": " + str(stdev(vet)))
    print("variance " + sm + ": " + str(variance(vet)))
    print("\n=====================================================================\n")



    
    
    