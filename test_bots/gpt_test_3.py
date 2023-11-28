from qiskit import QuantumCircuit, Aer, transpile, assemble

# Function to add two numbers using a quantum circuit
def quantum_addition(input1, input2):
    # Quantum circuit with 3 qubits (2 for input, 1 for output)
    circuit = QuantumCircuit(3, 3)

    # Encode inputs in superposition
    circuit.h(0)
    circuit.h(1)

    # Perform addition using Quantum Fourier Transform
    circuit.ccx(0, 1, 2)  # Controlled-X gate (Toffoli) for addition
    circuit.cx(0, 1)  # Classical XOR for addition
    circuit.barrier()

    # Measure the result
    circuit.measure([0, 1, 2], [0, 1, 2])

    # Transpile the circuit for the simulator
    transpiled_circuit = transpile(circuit, Aer.get_backend('qasm_simulator'))

    # Run the simulation
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(transpiled_circuit).result()

    # Get the counts from the result
    counts = result.get_counts(circuit)

    return counts

# Test the function with input (2, 2)
result_counts = quantum_addition(2, 2)

# Print the result
print("Result:", result_counts)

# Extract the output bitstring
output_bitstring = list(result_counts.keys())[0]

# Display the output
print("Output:", output_bitstring)
