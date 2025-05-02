# Analyzing the usage of Cython vs Python for the collection of metrics on PC and Android

## Why Cython?
> Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself.
>> From [Cython.org](https://cython.org/)

The usage of Cython was considered due to concerns regarding the noise the app could generate on the metrics it collects. Therefore, another version of the app's source code, including `cpdef` function calls and static typing, was written, with the purpose of comparing Cython and Python for the purposes of the app.

## Benchmarking
In this project, the `timeit` Python library was utilized to measure the time spent on 20k executions of each callback called by both Cython and Python versions of the app. The results for each goes as followed:

### Python
```bash
Benchmark Results:
cpu: 0.515711 seconds
ram: 0.553000 seconds
disk: 4.181701 seconds
disk_read: 4.091273 seconds
disk_write: 4.241761 seconds
network_recv: 1.032085 seconds
network_sent: 1.110684 seconds
```

```bash
Mean and Standard Deviation of Benchmark Results:
cpu: 0.540373 ± 0.019174 seconds
ram: 0.566320 ± 0.008887 seconds
disk: 4.077550 ± 0.125483 seconds
disk_read: 4.147758 ± 0.101581 seconds
disk_write: 4.048152 ± 0.053619 seconds
network_recv: 1.025356 ± 0.033519 seconds
network_sent: 1.015779 ± 0.028400 seconds
```

### Cython
```bash
Benchmark Results:
cpu: 0.531325 seconds
ram: 0.563645 seconds
disk: 4.030589 seconds
disk_read: 4.019378 seconds
disk_write: 4.013327 seconds
network_recv: 1.024371 seconds
network_sent: 1.032081 seconds
```

```bash
Mean and Standard Deviation of Benchmark Results:
cpu: 0.542532 ± 0.009208 seconds
ram: 0.574835 ± 0.012645 seconds
disk: 4.069354 ± 0.052873 seconds
disk_read: 4.048668 ± 0.047457 seconds
disk_write: 4.058806 ± 0.057552 seconds
network_recv: 1.019336 ± 0.012465 seconds
network_sent: 1.026059 ± 0.022183 seconds
```

As we can see, there is **no significant improval** of performance with the usage of Cython; in fact, it is plausible to say the two versions of the app perform **exactly the same**. This probably occurs because the metric collecting and processing app does not execute constant **CPU-bound** operations, which benefit heavily from Cython's optimization capabilites, instead, relying on I/O calls and libraries that are probably already written in C or Cython. Considering that developing in Cython comes with its own set of cons, such as difficulty debugging due to compilation and reduced code readability, we will not keep on using Cython moving forward.