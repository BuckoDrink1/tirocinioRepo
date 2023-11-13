from quantum_circuit_to_matrix import Justify, qc2matrix
from qiskit import qpy
from qiskit import QuantumCircuit, QuantumRegister
import time

i = 0
lim = 468

while(i <= lim):
    with open('circuit' + str(i) + '.qpy', 'rb') as fd:
        qc = qpy.load(fd)[0]
        qc2matrix(qc, Justify.none, 'mat' + str(i) + '.csv')
        i = i + 1
        time.sleep(2)