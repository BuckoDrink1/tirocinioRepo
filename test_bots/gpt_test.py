from qiskit import QuantumCircuit, Aer, transpile, assemble

def add_two_bits():
    # Create a quantum circuit with two input bits and one output bit
    qc = QuantumCircuit(3, 3)

    # Initialize input bits to |2> in binary (|10>)
    qc.x(0)

    # Apply quantum operations to perform addition
    qc.cx(0, 2)  # CNOT gate to copy the value of the first bit to the third bit
    qc.cx(1, 2)  # CNOT gate to copy the value of the second bit to the third bit
    qc.barrier()  # Barrier for visual separation

    # Measure the result
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)


    return qc

# Visualize the quantum circuit
quantum_circuit = add_two_bits()
print("Quantum Circuit:")
print(quantum_circuit)

# Simulate the quantum circuit
simulator = Aer.get_backend('qasm_simulator')
tqc = transpile(quantum_circuit, simulator)
result = simulator.run(tqc).result()

# Display the result in binary
counts = result.get_counts()
binary_result = list(counts.keys())[0]
print("\nResult in Binary:", binary_result)
