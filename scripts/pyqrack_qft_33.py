# See https://blog.hpc.qmul.ac.uk/pyfftw.html
import time
from pyqrack import QrackSimulator

width = 10
samples = 100

def reverse_qrack(sim):
    start = 0
    end = sim.num_qubits() - 1
    while (start < end):
        sim.swap(start, end)
        start += 1
        end -= 1

def bench_qrack(n):
    sim = QrackSimulator(n)
    sim.h(0)
    for i in range(n - 1):
        sim.mcx([i], i + 1)
    start = time.perf_counter()
    qubits = [i for i in range(n)]
    sim.qft(qubits)
    reverse_qrack(sim)
    sim.m_all()

    return time.perf_counter() - start

qrack_results = []
for i in range(samples):
    qrack_results.append(bench_qrack(width))

print(sum(qrack_results) / samples)
