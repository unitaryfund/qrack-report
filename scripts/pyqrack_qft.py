#Adapted from https://github.com/libtangle/qcgpu/blob/master/benchmark/benchmark.py by Adam Kelly

import click
import time
import random
import csv
import os.path
import math

from pyqrack import QrackSimulator, Pauli

# NOTE - |0> or any permutation basis eigenstate QFT is "trivial" for Qrack, and not a fairly
#  representative test of general QFT performance, in realistic use cases. Hence, this script
#  applies a random unitary gate to every qubit in the width before carrying out the QFT.
#  As a result, every other simulator gets a significant handicap, but a representative one.

def bench(sim):
    sim.reset_all()
    num_qubits = sim.num_qubits()
    # |0> state QFT is "trivial" for Qrack, so we give it a realistic case instead.
    for i in range(num_qubits):
        # Initialize with uniformly random single qubit gates, across full width.
        sim.u(i, random.uniform(0, 2 * math.pi), random.uniform(0, 2 * math.pi), random.uniform(0, 2 * math.pi))
    start = time.time()
    qubits = [i for i in range(num_qubits)]
    sim.qft(qubits)
    sim.m_all()

    return time.time() - start

# Reporting
def create_csv(filename):
    file_exists = os.path.isfile(filename)
    csvfile = open(filename, 'a')
   
    headers = ['name', 'num_qubits', 'time']
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)

    if not file_exists:
        writer.writeheader()  # file doesn't exist yet, write a header

    return writer

def write_csv(writer, data):
    writer.writerow(data)



@click.command()
@click.option('--samples', default=100, help='Number of samples to take for each qubit.')
@click.option('--qubits', default=28, help='How many qubits you want to test for')
@click.option('--out', default='benchmark_data.csv', help='Where to store the CSV output of each test')
@click.option('--single', default=False, help='Only run the benchmark for a single amount of qubits, and print an analysis')
def benchmark(samples, qubits, out, single):
    if single:
        low = qubits - 1
    else:
        low = 3
    high = qubits

    functions = bench,
    writer = create_csv(out)

    for n in range(low, high):
        sim = QrackSimulator(n + 1)

        # Progress counter
        progress = (n - low) / (high - low)
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress*100), end="", flush=True)

        # Run the benchmarks
        for i in range(samples):
            try:
                t = bench(sim)
                write_csv(writer, {'name': 'pyqrack_qft', 'num_qubits': n+1, 'time': t})
            except:
                del sim
                write_csv(writer, {'name': 'pyqrack_qft', 'num_qubits': n+1, 'time': -999})
                sim = QrackSimulator(n + 1)

        # Call old simulator width destructor BEFORE initializing new width
        del sim

if __name__ == '__main__':
    benchmark()
