from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, transpile

def simulate_circuit(adder_circuit):
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(adder_circuit, simulator)
    result = simulator.run(transpiled_circuit).result()
    counts = result.get_counts()
    return counts

# Create 3 qubit quantum register
q = QuantumRegister(3, 'q')

# Create 2 bit classical register to store result
c = ClassicalRegister(2, 'c')

# Create quantum circuit
circ = QuantumCircuit(q, c)

# Add 2 and 2 using quantum adder circuit
circ.x(q[0])  # Set first qubit to |1> (represents 2)
circ.x(q[1])  # Set second qubit to |1> (represents 2)

#circ.h(q[0])
#circ.h(q[1])
#circ.h(q[2])

circ.ccx(q[0], q[1], q[2])

# Measure result in computational basis and store in classical register
circ.measure(q[0], c[0])
circ.measure(q[1], c[1])

# Draw circuit
display(circ.draw('mpl'))

def display_result(counts):
    for state, count in counts.items():
        print(f"Result: {state}, Count: {count}")

# Main function
def main():
    counts = simulate_circuit(circ)
    display_result(counts)

if __name__ == "__main__":
    main()