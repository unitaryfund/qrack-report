# See https://blog.hpc.qmul.ac.uk/pyfftw.html
import pyfftw
import time
import numpy as np

width = 33
samples = 100

pyfftw.interfaces.cache.enable()
pyfftw.interfaces.cache.set_keepalive_time(60)
total_time = 0

fftw_results = []
for i in range(samples):
    io_array = pyfftw.empty_aligned(2**width, dtype=np.complex64)
    io_array[0] = 1.
    start = time.perf_counter()
    pyfftw.interfaces.numpy_fft.fft(io_array, overwrite_input=True, threads = 48)
    fftw_results.append(time.perf_counter() - start)

print(sum(fftw_results) / samples)
