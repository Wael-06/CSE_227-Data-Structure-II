# CSE 227 — Data Structures II

A benchmarking tool for evaluating sorting algorithms across different input sizes.

## Usage

Requires `clang++` and `pypy3`.
`g++` and standard Python can also be used but not recommended .

```bash
clang++ generator.cpp -o generator
./generator
pypy3 template_for_py.py
```

## Project Structure

- `algos/` — algorithm implementations.
- `arrays/` — Generated test arrays (created at runtime).
- `results.csv` — Benchmark results: mean and standard deviation of runtime, comparisons, writes, and correctness.
- `Reports/` — Graphs comparing algorithms across input sizes.

The benchmark generates random test arrays, runs the algorithms, and records performance results.
