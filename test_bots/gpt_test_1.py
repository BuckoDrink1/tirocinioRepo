from qiskit import QuantumCircuit, Aer, transpile, assemble

# Create a quantum circuit with 4 qubits (2 for each input) and 3 classical bits (for the output)
qc = QuantumCircuit(4, 3)

# Apply Hadamard gate to the first two qubits to create a superposition of all possible inputs
qc.h([0, 1])

# Apply a controlled-X gate to simulate addition (using XOR logic)
qc.cx(0, 2)
qc.cx(1, 2)

# Apply a Toffoli gate to perform the final addition
qc.ccx(0, 1, 3)
qc.cx(1, 2)

# Measure the output qubits
qc.measure([2, 3, 0], [0, 1, 2])

# Choose the simulator backend
backend = Aer.get_backend('qasm_simulator')

# Transpile the circuit for the simulator
tqc = transpile(qc, backend)

# Run the simulation
result = backend.run(tqc).result()

# Get the counts of the measurement outcomes
counts = result.get_counts()

# Print the result
print("Measurement outcome:", list(counts.keys())[0])
