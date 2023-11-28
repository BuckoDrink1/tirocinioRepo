from qiskit import QuantumCircuit, Aer, transpile, assemble

def add(a, b):
    # Determine the number of qubits needed to represent the sum
    n = len(bin(max(a, b))) - 2

    # Create a quantum circuit with n+2 qubits (2 extra for carry)
    qc = QuantumCircuit(n + 2, n)

    # Initialize input values in binary representation
    a_bin = format(a, '0' + str(n) + 'b')
    b_bin = format(b, '0' + str(n) + 'b')

    # Initialize quantum circuit with input values
    for i in range(n):
        if a_bin[n - 1 - i] == '1':
            qc.x(i)
        if b_bin[n - 1 - i] == '1':
            qc.x(n + i)

    # Apply quantum addition
    for i in range(n):
        qc.ccx(i, n + i, n + 1 + i)
        qc.cx(i, n + i)
        qc.ccx(i, n + i, n + 1 + i)

    # Measure the sum
    qc.measure(range(n + 2, 2 * n + 2), range(n))

    # Simulate the quantum circuit
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit).result()

    # Get the binary representation of the result
    counts = result.get_counts(qc)
    binary_sum = max(counts, key=counts.get)

    return binary_sum

# Test the add function
a = 2
b = 2
result = add(a, b)

print(f"The sum of {a} and {b} is {int(result, 2)} in decimal, and the binary representation is {result}")
