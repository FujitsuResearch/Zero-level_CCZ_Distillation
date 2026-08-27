import json, io
import numpy as np
from qulacs import QuantumState, QuantumCircuit, Observable
from qulacs.gate import H, RY, CNOT, T, Tdag, X, Z, SWAP
from qulacs.gate import BitFlipNoise, DephasingNoise, TwoQubitDepolarizingNoise, DepolarizingNoise
from qulacs.gate import Measurement
from qulacs.state import inner_product, drop_qubit

stabilizer = [Observable(8) for i in range(5)]
logical_operator = [Observable(8) for i in range(6)]
stabilizer[0].add_operator(1., "X 0 X 1 X 2 X 3 X 4 X 5 X 6 X 7")
stabilizer[1].add_operator(1., "Z 0 Z 1 Z 2 Z 3")
stabilizer[2].add_operator(1., "Z 4 Z 5 Z 6 Z 7")
stabilizer[3].add_operator(1., "Z 0 Z 1 Z 4 Z 5")
stabilizer[4].add_operator(1., "Z 0 Z 2 Z 4 Z 6")
logical_operator[0].add_operator(1., "Z 0 Z 4")
logical_operator[1].add_operator(1., "X 0 X 1 X 2 X 3")
logical_operator[2].add_operator(1., "Z 0 Z 2")
logical_operator[3].add_operator(1., "X 0 X 1 X 4 X 5")
logical_operator[4].add_operator(1., "Z 0 Z 1")
logical_operator[5].add_operator(1., "X 0 X 2 X 4 X 6")

def reset_z(circuit, qubit, p):
    circuit.add_gate(BitFlipNoise(qubit, p))
    
def reset_x(circuit, qubit, p):
    circuit.add_gate(H(qubit))
    circuit.add_gate(DephasingNoise(qubit, p))

def cx(circuit, qubit1, qubit2, p):
    circuit.add_gate(CNOT(qubit1, qubit2))
    circuit.add_gate(TwoQubitDepolarizingNoise(qubit1, qubit2, p))

def mes_z(circuit, qubit, index,  p):
    circuit.add_gate(BitFlipNoise(qubit, p))
    circuit.add_gate(Measurement(qubit, index))
    
def mes_x(circuit, qubit, index, p):
    circuit.add_gate(H(qubit))
    circuit.add_gate(BitFlipNoise(qubit, p))
    circuit.add_gate(Measurement(qubit, index))

def mes_reset_z(circuit, qubit, index, p):
    circuit.add_gate(BitFlipNoise(qubit, p))
    circuit.add_gate(Measurement(qubit, index))
    circuit.add_gate(BitFlipNoise(qubit, p))
    
    
def mes_reset_x(circuit, qubit, index, p):
    circuit.add_gate(H(qubit))
    circuit.add_gate(BitFlipNoise(qubit, p))
    circuit.add_gate(Measurement(qubit, index))
    circuit.add_gate(H(qubit))
    circuit.add_gate(DephasingNoise(qubit, p))
    
def t(circuit, qubit, p):
    circuit.add_gate(T(qubit))
    circuit.add_gate(DepolarizingNoise(qubit, p))

def tdag(circuit, qubit, p):
    circuit.add_gate(Tdag(qubit))
    circuit.add_gate(DepolarizingNoise(qubit, p))

def idling(circuit, qubits, p):
    for qubit in qubits:
        circuit.add_gate(DepolarizingNoise(qubit, p))
        
mode = "ccz"
# mode = "ppp"
logical_error = 0
detect = 0
loop = 10 ** 5
# loop = 1

state_non_error = QuantumState(16)
circuit_non_error = QuantumCircuit(16)

circuit_non_error.add_gate(H(1))
circuit_non_error.add_gate(H(3))
circuit_non_error.add_gate(H(4))
circuit_non_error.add_gate(H(6))

circuit_non_error.add_gate(CNOT(4, 0))
circuit_non_error.add_gate(CNOT(1, 5))
circuit_non_error.add_gate(CNOT(6, 7))
circuit_non_error.add_gate(CNOT(3, 2))

circuit_non_error.add_gate(CNOT(2, 0))
circuit_non_error.add_gate(CNOT(1, 3))
circuit_non_error.add_gate(CNOT(6, 4))
circuit_non_error.add_gate(CNOT(5, 7))

circuit_non_error.add_gate(CNOT(0, 1))
circuit_non_error.add_gate(CNOT(4, 5))

if mode == "ccz":
    circuit_non_error.add_gate(T(0))
    circuit_non_error.add_gate(Tdag(1))
    circuit_non_error.add_gate(Tdag(2))
    circuit_non_error.add_gate(T(3))
    circuit_non_error.add_gate(Tdag(4))
    circuit_non_error.add_gate(T(5))
    circuit_non_error.add_gate(T(6))
    circuit_non_error.add_gate(Tdag(7))

circuit_non_error.update_quantum_state(state_non_error)

for _ in range(loop):
    p = 1e-3
    # p = 0
    state_error = QuantumState(16)
    circuit_error = QuantumCircuit(16)

    # 1
    reset_z(circuit_error, 4, p)
    reset_z(circuit_error, 5, p)
    reset_x(circuit_error, 6, p)
    reset_x(circuit_error, 7, p)
    reset_x(circuit_error, 8, p)
    reset_x(circuit_error, 9, p)
    reset_z(circuit_error, 10, p)
    reset_z(circuit_error, 11, p)

    # 2
    cx(circuit_error, 8, 4, p)
    cx(circuit_error, 6, 5, p)
    cx(circuit_error, 9, 10, p)
    cx(circuit_error, 7, 11, p)

    # 3
    cx(circuit_error, 4, 5, p)
    cx(circuit_error, 7, 6, p)
    cx(circuit_error, 9, 8, p)
    cx(circuit_error, 10, 11, p)
    
    # 4
    cx(circuit_error, 5, 9, p)
    cx(circuit_error, 6, 10, p)
    reset_x(circuit_error, 0, p)
    reset_x(circuit_error, 1, p)
    reset_x(circuit_error, 2, p)
    reset_x(circuit_error, 3, p)
    reset_x(circuit_error, 12, p)
    reset_x(circuit_error, 13, p)
    reset_x(circuit_error, 14, p)
    reset_x(circuit_error, 15, p)
    idling(circuit_error, [4, 7, 8, 11], p)

    # 5
    cx(circuit_error, 0, 4, p)
    cx(circuit_error, 1, 5, p)
    cx(circuit_error, 2, 6, p)
    cx(circuit_error, 3, 7, p)
    cx(circuit_error, 12, 8, p)
    cx(circuit_error, 13, 9, p)
    cx(circuit_error, 14, 10, p)
    cx(circuit_error, 15, 11, p)
    
    # 6
    cx(circuit_error, 5, 9, p)
    cx(circuit_error, 6, 10, p)
    idling(circuit_error, [4, 7, 8, 11], p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)
    
    # 7
    cx(circuit_error, 4, 5, p)
    cx(circuit_error, 7, 6, p)
    cx(circuit_error, 9, 8, p)
    cx(circuit_error, 10, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)
    
    # 8
    cx(circuit_error, 8, 4, p)
    cx(circuit_error, 6, 5, p)
    cx(circuit_error, 9, 10, p)
    cx(circuit_error, 7, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)
    
    # 9
    mes_reset_x(circuit_error, 6, 0, p)
    mes_reset_x(circuit_error, 7, 1, p)
    mes_reset_x(circuit_error, 8, 2, p)
    mes_reset_x(circuit_error, 9, 3, p)
    idling(circuit_error, [4, 5, 10, 11], p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)

    # 10
    cx(circuit_error, 8, 4, p)
    cx(circuit_error, 6, 5, p)
    cx(circuit_error, 9, 10, p)
    cx(circuit_error, 7, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)

    # 11
    cx(circuit_error, 4, 5, p)
    cx(circuit_error, 7, 6, p)
    cx(circuit_error, 9, 8, p)
    cx(circuit_error, 10, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 12, 13, 14, 15], p)

    # 12
    cx(circuit_error, 5, 9, p)
    cx(circuit_error, 6, 10, p)

    cx(circuit_error, 4, 0, p)
    cx(circuit_error, 7, 3, p)
    cx(circuit_error, 8, 12, p)
    cx(circuit_error, 11, 15, p)
    idling(circuit_error, [1, 2, 13, 14], p)

    # 13
    cx(circuit_error, 5, 1, p)
    cx(circuit_error, 6, 2, p)
    cx(circuit_error, 13, 9, p)
    cx(circuit_error, 10, 14, p)
    mes_x(circuit_error, 4, 4, p)
    mes_x(circuit_error, 7, 5, p)
    mes_x(circuit_error, 8, 6, p)
    mes_x(circuit_error, 11, 7, p)
    idling(circuit_error, [0, 3, 12, 15], p)
    
    # 14
    mes_x(circuit_error, 5, 8, p)
    mes_x(circuit_error, 6, 9, p)
    mes_x(circuit_error, 10, 10, p)
    mes_x(circuit_error, 13, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 9, 12, 14, 15], p)
    
    circuit_error.update_quantum_state(state_error)
    mes_result = []
    for i in range(12):
        mes_result.append(state_error.get_classical_value(i))
    # print(mes_result)
    if any(mes_result):
        detect += 1
        continue

    circuit_error = QuantumCircuit(16)
    # 15
    reset_x(circuit_error, 5, p)
    reset_z(circuit_error, 6, p)
    idling(circuit_error, [0, 1, 2, 3, 9, 12, 14, 15], p)

    # 16
    cx(circuit_error, 5, 6, p)
    reset_z(circuit_error, 4, p)
    reset_z(circuit_error, 7, p)
    reset_z(circuit_error, 8, p)
    reset_z(circuit_error, 10, p)
    reset_z(circuit_error, 11, p)
    if mode == "ccz":
        t(circuit_error, 1, p)
        tdag(circuit_error, 9, p)
        tdag(circuit_error, 0, p)
        t(circuit_error, 12, p)
        tdag(circuit_error, 2, p)
        t(circuit_error, 14, p)
        t(circuit_error, 3, p)
        tdag(circuit_error, 15, p)
    elif mode == "ppp":
        idling(circuit_error, [0, 1, 2, 3, 9, 12, 14, 15], p)
        
    # 17
    cx(circuit_error, 5, 4, p)
    cx(circuit_error, 6, 7, p)
    cx(circuit_error, 12, 8, p)
    cx(circuit_error, 14, 10, p)
    cx(circuit_error, 15, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 9], p)
    
    # 18
    cx(circuit_error, 4, 8, p)
    cx(circuit_error, 5, 9, p)
    cx(circuit_error, 6, 10, p)
    cx(circuit_error, 7, 11, p)
    idling(circuit_error, [0, 1, 2, 3, 12, 14, 15], p)
    
    # 19
    cx(circuit_error, 4, 0, p)
    cx(circuit_error, 5, 1, p)
    cx(circuit_error, 6, 2, p)
    cx(circuit_error, 7, 3, p)
    reset_z(circuit_error, 13, p)
    mes_x(circuit_error, 12, 0, p)
    mes_reset_x(circuit_error, 14, 1, p)
    mes_x(circuit_error, 15, 2, p)
    idling(circuit_error, [9], p)
    
    circuit_error.update_quantum_state(state_error)
    circuit_error = QuantumCircuit(16)
    mes_result = []
    for i in range(3):
        mes_result.append(state_error.get_classical_value(i))

    if mes_result[0] == 1:
        circuit_error.add_gate(Z(4))
        circuit_error.add_gate(Z(8))
        circuit_error.add_gate(X(12))
    if mes_result[1] == 1:
        circuit_error.add_gate(Z(6))
        circuit_error.add_gate(Z(10))
        circuit_error.add_gate(Z(14))
    if mes_result[2] == 1:
        circuit_error.add_gate(Z(7))
        circuit_error.add_gate(Z(11))
        circuit_error.add_gate(X(15))
        
        
    # 20
    cx(circuit_error, 8, 4, p)
    cx(circuit_error, 9, 5, p)
    cx(circuit_error, 10, 6, p)
    cx(circuit_error, 11, 7, p)
    cx(circuit_error, 14, 13, p)
    reset_z(circuit_error, 12, p)
    reset_z(circuit_error, 15, p)
    idling(circuit_error, [0, 1, 2, 3], p)
    
    # 21
    cx(circuit_error, 0, 4, p)
    cx(circuit_error, 1, 5, p)
    cx(circuit_error, 2, 6, p)
    cx(circuit_error, 3, 7, p)
    cx(circuit_error, 8, 12, p)
    cx(circuit_error, 9, 13, p)
    cx(circuit_error, 10, 14, p)
    cx(circuit_error, 11, 15, p)
    
    # 22
    cx(circuit_error, 5, 4, p)
    cx(circuit_error, 6, 7, p)
    cx(circuit_error, 12, 13, p)
    cx(circuit_error, 15, 14, p)
    mes_x(circuit_error, 8, 0, p)
    mes_x(circuit_error, 11, 1, p)

    circuit_error.update_quantum_state(state_error)
    circuit_error = QuantumCircuit(16)
    mes_result = []
    for i in range(2):
        mes_result.append(state_error.get_classical_value(i))

    if mes_result[0] == 1:
        circuit_error.add_gate(Z(12))
        circuit_error.add_gate(X(8))
    if mes_result[1] == 1:
        circuit_error.add_gate(Z(15))
        circuit_error.add_gate(X(11))

    # 23
    cx(circuit_error, 5, 6, p)
    cx(circuit_error, 13, 14, p)
    mes_z(circuit_error, 4, 0, p)
    mes_z(circuit_error, 7, 1, p)

    # 24
    mes_x(circuit_error, 5, 2, p)
    mes_z(circuit_error, 6, 3, p)
    mes_x(circuit_error, 13, 4, p)
    mes_z(circuit_error, 14, 5, p)

    circuit_error.add_gate(SWAP(0, 1))
    circuit_error.add_gate(SWAP(1, 9))
    circuit_error.add_gate(SWAP(9, 2))
    circuit_error.add_gate(SWAP(3, 12))
    circuit_error.add_gate(SWAP(4, 9))
    circuit_error.add_gate(SWAP(5, 10))
    circuit_error.add_gate(SWAP(6, 12))
    circuit_error.add_gate(SWAP(7, 15))

    circuit_error.update_quantum_state(state_error)
    mes_result = []
    for i in range(6):
        mes_result.append(state_error.get_classical_value(i))
    # print(mes_result)
    if any(mes_result):
        detect += 1
        continue

    # for i in range(8, 16):
    #     state_error = drop_qubit(state_error, [8], [0])
        
    circuit_error = QuantumCircuit(16)
    # syndrome measurement
    for i in range(7):
        circuit_error.add_gate(CNOT(i + 1, i + 0))
    circuit_error.add_gate(H(7))
    circuit_error.add_gate(Measurement(7, 0))
    circuit_error.add_gate(H(7))
    for i in range(6, -1, -1):
        circuit_error.add_gate(CNOT(i + 1, i + 0))

    circuit_error.add_gate(CNOT(0, 1))
    circuit_error.add_gate(CNOT(1, 2))
    circuit_error.add_gate(CNOT(2, 3))
    circuit_error.add_gate(Measurement(3, 1))
    circuit_error.add_gate(CNOT(2, 3))
    circuit_error.add_gate(CNOT(1, 2))
    circuit_error.add_gate(CNOT(0, 1))

    circuit_error.add_gate(CNOT(4, 5))
    circuit_error.add_gate(CNOT(5, 6))
    circuit_error.add_gate(CNOT(6, 7))
    circuit_error.add_gate(Measurement(7, 2))
    circuit_error.add_gate(CNOT(6, 7))
    circuit_error.add_gate(CNOT(5, 6))
    circuit_error.add_gate(CNOT(4, 5))

    circuit_error.add_gate(CNOT(0, 1))
    circuit_error.add_gate(CNOT(1, 4))
    circuit_error.add_gate(CNOT(4, 5))
    circuit_error.add_gate(Measurement(5, 3))
    circuit_error.add_gate(CNOT(4, 5))
    circuit_error.add_gate(CNOT(1, 4))
    circuit_error.add_gate(CNOT(0, 1))

    circuit_error.add_gate(CNOT(0, 2))
    circuit_error.add_gate(CNOT(2, 4))
    circuit_error.add_gate(CNOT(4, 6))
    circuit_error.add_gate(Measurement(6, 4))
    circuit_error.add_gate(CNOT(4, 6))
    circuit_error.add_gate(CNOT(2, 4))
    circuit_error.add_gate(CNOT(0, 2))

    circuit_error.update_quantum_state(state_error)

    mes_result = []
    for i in range(4):
        mes_result.append(state_error.get_classical_value(i))
    # print(mes_result)
    if any(mes_result):
        detect += 1
        continue
    
    
    # print(abs(inner_product(state_non_error, state_error)))
    if(abs(inner_product(state_non_error, state_error)) < 0.999):
        logical_error += 1
        # print(mes_result)
        # print(abs(inner_product(state_non_error, state_error)) )

if mode == "ccz":
    path = "ccz"
elif mode == "ppp":
    path = "ppp"
    
with open(f'15_{path}.json') as f:
    try:
        data = json.load(f)
    except (io.UnsupportedOperation, json.JSONDecodeError):
        data = {}
    data[p] = {"logical_error_rate": logical_error / (loop - detect), "success_rate": (loop - detect) / loop, "iteration": loop, "logical_error": logical_error, "detect": detect}
with open(f'15_{path}.json', 'w') as f:
    json.dump(data, f, indent=2)

print(logical_error)
print(detect)
print((loop - detect) / loop)
print(logical_error / (loop - detect))