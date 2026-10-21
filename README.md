# CSE 227 — Data Structures II

A benchmarking tool for evaluating algorithms across different input sizes.

## Usage

Requires `clang++` and `pypy3`.
standard Python can also be used but not recommended .
Note: If using `g++`, update the `generate_arrays()` function in `benchmarker_for_py.py`. 

```bash
./generator
pypy3 benchmarker_for_py.py
```

## Project Structure

- `algos/` — algorithm implementations.
- `arrays/` — Generated test arrays (created at runtime).
- `results.csv` — Benchmark results: mean and standard deviation of runtime, comparisons, writes, and correctness.
- `Reports/` — Graphs comparing algorithms across input sizes.

The benchmark generates random test arrays, runs the algorithms, and records performance results.
