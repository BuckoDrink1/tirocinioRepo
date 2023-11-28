from qiskit import QuantumCircuit, Aer, transpile, assemble

# Define the quantum circuit
def create_adder_circuit():
    n = 3  # Number of qubits

    # Create quantum and classical registers
    qc = QuantumCircuit(n, n)

    # Apply Hadamard gate to all qubits
    qc.h(range(n))

    # Apply X gate to the target qubit (qubit 2 in 0-based indexing)
    qc.x(2)

    # Apply controlled-X gates
    qc.cx(0, 2)
    qc.cx(1, 2)

    # Apply controlled-Z gate
    qc.cz(0, 1)

    # Measure the qubits
    qc.measure(range(n), range(n))

    return qc

# Simulate the quantum circuit
def simulate_circuit(adder_circuit):
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(adder_circuit, simulator)
    qobj = assemble(transpiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts()
    return counts

# Display the result
def display_result(counts):
    for state, count in counts.items():
        if state == '100':
            print(f"Result: {state}, Count: {count}")

# Main function
def main():
    adder_circuit = create_adder_circuit()
    counts = simulate_circuit(adder_circuit)
    display(adder_circuit.draw('mpl'))
    display_result(counts)

if __name__ == "__main__":
    main()
