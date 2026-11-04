from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def build_qps_puzzle_oracle():
    """Simulates a production rule checking if a move is valid."""
    qc = QuantumCircuit(3)
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    return qc

qps_circuit = QuantumCircuit(3)

# Create superposition of all puzzle states
qps_circuit.h(range(3))

# Oracle (production rule)
oracle = build_qps_puzzle_oracle()
qps_circuit.compose(oracle, inplace=True)

# Diffuser (Grover amplification)
diffuser = QuantumCircuit(3)
diffuser.h(range(3))
diffuser.x(range(3))
diffuser.h(2)
diffuser.ccx(0, 1, 2)
diffuser.h(2)
diffuser.x(range(3))
diffuser.h(range(3))

qps_circuit.compose(diffuser, inplace=True)

# Measure all qubits
qps_circuit.measure_all()
print(qps_circuit.draw())
# Simulation
simulator = AerSimulator()
compiled_circuit = transpile(qps_circuit, simulator)

job = simulator.run(compiled_circuit, shots=1024)

result = job.result().get_counts()

print("QPS Rule Matching Output:", result)