from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, transpile


# Initialize quantum and classical registers
qr = QuantumRegister(4, 'qr')
cr = ClassicalRegister(4, 'cr')
qc = QuantumCircuit(qr, cr)

# Initialize qubits representing inputs
qc.x(qr[2]) # Input 1 = 10 
qc.x(qr[3]) # Input 2 = 10

# Apply adder quantum circuit
qc.cx(qr[2], qr[0])
qc.cx(qr[3], qr[1])
qc.ccx(qr[2], qr[3], qr[0])
qc.ccx(qr[2], qr[3], qr[1])

# Measure output
qc.measure(qr[0], cr[0]) 
qc.measure(qr[1], cr[1])
qc.measure(qr[2], cr[2]) #ho aggiunto queste altre due misure, perchè senza è ovviamente sbagliato
qc.measure(qr[3], cr[3])


display(qc.draw('mpl'))

def simulate_circuit(adder_circuit):
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(adder_circuit, simulator)
    result = simulator.run(transpiled_circuit).result()
    counts = result.get_counts()
    return counts

def display_result(counts):
    for state, count in counts.items():
        print(f"Result: {state}, Count: {count}")

# Main function
def main():
    counts = simulate_circuit(qc)
    display_result(counts)

if __name__ == "__main__":
    main()