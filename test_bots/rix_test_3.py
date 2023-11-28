import qiskit

qc = qiskit.QuantumCircuit(4, 3)

# Initialize qubits
qc.x(0) 
qc.x(2)

# Carry out adder logic
qc.cx(0, 2)
qc.cx(1, 2)
qc.ccx(0, 1, 3)

qc.measure(qc.qubits[0:3], qc.clbits[0:3])

display(qc.draw('mpl'))

result = qiskit.Aer.get_backend('qasm_simulator').run(qc).result()
print(result.get_counts(qc))