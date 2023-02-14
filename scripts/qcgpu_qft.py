#Reduced directly from https://github.com/libtangle/qcgpu/blob/master/benchmark/benchmark.py by Adam Kelly (with thanks)

import click
import time
import random
import statistics
import csv
import os.path
import math

import qcgpu

def bench(num_qubits):
    start = time.time()
    state = qcgpu.State(num_qubits)

    for j in range(num_qubits):
        for k in range(j):
            state.cu1(j, k, math.pi/float(2**(j-k)))
        state.h(j)
    state.measure()

    state.backend.queue.finish()
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
        # Progress counter
        progress = (n - low) / (high - low)
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress*100), end="", flush=True)

        # Run the benchmarks
        for i in range(samples):
            func = random.choice(functions)
            t = func(n + 1)
            write_csv(writer, {'name': 'qcgpu_qft', 'num_qubits': n+1, 'time': t})

if __name__ == '__main__':
    benchmark()
