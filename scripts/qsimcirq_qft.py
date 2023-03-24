import time
import random
import math
import cirq
import qsimcirq
import cupy


low = 1
high = 27
samples = 10

def cuquantum_qft(q):
    qreg = list(q)
    for j in reversed(range(len(qreg))):
        yield cirq.H(qreg[j])
        for k in range(j):
            yield (cirq.CZ ** (2**(j-k)))(qreg[k], qreg[j])

    start = 0
    end = len(qreg) - 1
    while (start < end):
        yield cirq.SWAP(qreg[start], qreg[end])
        start += 1
        end -= 1

    yield cirq.measure(*qreg)

def bench_cuquantum(n):
    qubits = cirq.LineQubit.range(n)
    qft = cirq.Circuit(cuquantum_qft(qubits))
    simulator = qsimcirq.QSimSimulator(qsimcirq.QSimOptions(gpu_mode=1))

    start = time.perf_counter()
    simulator.run(qft, repetitions=1)
    return time.perf_counter() - start

qsimcirq_results = {}
for n in range(low, high + 1):
    width_results = []
         
    # Run the benchmarks
    for i in range(samples):
        width_results.append(bench_cuquantum(n))

    qsimcirq_results[n] = sum(width_results) / samples

print(qsimcirq_results)
