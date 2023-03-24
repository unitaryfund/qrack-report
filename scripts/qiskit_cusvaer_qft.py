import time
import random
import math
from qiskit import QuantumCircuit
from qiskit import execute
from cusvaer.backends import StatevectorSimulator

low = 1
high = 27
samples = 10

def reverse_aer(num_qubits, circ):
    start = 0
    end = num_qubits - 1
    while (start < end):
        circ.swap(start, end)
        start += 1
        end -= 1

# Implementation of the Quantum Fourier Transform
# (See https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)
def aer_qft(n, circuit):
    if n == 0:
        return circuit
    n -= 1

    circuit.h(n)
    for qubit in range(n):
        circuit.cp(math.pi/2**(n-qubit), qubit, n)

    # Recursive QFT is very similiar to a ("classical") FFT
    aer_qft(n, circuit)

sim_backend = StatevectorSimulator(shots=1)
sim_backend.set_options(precision='single')

def bench_aer(num_qubits):
    circ = QuantumCircuit(num_qubits, num_qubits)
    aer_qft(num_qubits, circ)
    reverse_aer(num_qubits, circ)
    for j in range(num_qubits):
        circ.measure(j, j)
    start = time.perf_counter()
    job = execute([circ], sim_backend)
    result = job.result()
    return time.perf_counter() - start

aer_results = {}
for n in range(low, high + 1):
    width_results = []
        
    # Run the benchmarks
    for i in range(samples):
        width_results.append(bench_aer(n))

    aer_results[n] = sum(width_results) / samples

print(aer_results)

