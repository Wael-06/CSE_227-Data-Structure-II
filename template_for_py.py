import csv
import os
import glob
import time
import importlib.util
import matplotlib
matplotlib.use("Agg")  # for pypy
import matplotlib.pyplot as plt

ALGOS_DIR="algos"
ARRAYS_DIR="arrays"
REPORTS_DIR="Reports"
RESULTS_CSV="results.csv"

FIELDS=["algorithm", "n", "time_mean_ms", "time_std_ms","comparisons",
         "writes", "correct"]

SIZES=[500, 1000, 10000, 25000, 50000, 75000, 100000]


TRIALS=1

# modules in algos/ that expose a function
def discover_algos(algos_dir=ALGOS_DIR):
    algorithms = {}
    for filepath in sorted(glob.glob(os.path.join(algos_dir, "*.py"))):
        name = os.path.splitext(os.path.basename(filepath))[0]
        if name.startswith("_"):
            continue

        spec = importlib.util.spec_from_file_location(name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "sort"):
            algorithms[name] = module.sort
        else:
            print("[warn] " + filepath + 
                  " has no sort(arr) function -- skipping")
    return algorithms

# helpers
def load_array(path):
    with open(path) as f:
        return list(map(int, f.read().split()))
        #.split() splits the string around any whitespaces, \n, \t

def ensure_dirs():
    os.makedirs(REPORTS_DIR, exist_ok=True)


# Benchmarking
def benchmarking(func, src_arr, expected, trials):
    times = []
    correct = True
    comparisons = writes = None # as if fails 0 will ruin the benchmark, 
    # we want to know that it failed, not that it did 0 comparisons/writes 

    for _ in range(trials):
        arr = src_arr.copy()

        start = time.perf_counter()
        comparisons, writes = func(arr)
        end = time.perf_counter()

        times.append((end - start) * 1000)  # convert to ms

        if arr != expected:
            correct = False

    mean_ms = sum(times) / len(times) if times else 0.0
    if len(times) > 1:
        variance_value = sum((t - mean_ms) ** 2 for t in times) / (len(times) - 1)
        std_ms = variance_value ** 0.5
    else:
        std_ms = 0.0

    return {
        "time_mean_ms": mean_ms,
        "time_std_ms": std_ms,
        "comparisons": comparisons,
        "writes": writes,
        "correct": correct,
    }

def run_benchmarks(algorithms):
  ensure_dirs()

  with open(RESULTS_CSV, "w", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=FIELDS)
      writer.writeheader()
      f.flush()

      print(
          f"{'algorithm':<16} {'n':>8} {'mean_ms':>12} {'comparisons':>14} "
          f"{'writes':>12} {'ok':>5}"
      )

      for n in SIZES:
          input_path = os.path.join(ARRAYS_DIR, f"n{n}_input.txt")
          output_path = os.path.join(ARRAYS_DIR, f"n{n}_sorted.txt")

          if not (os.path.exists(input_path) and os.path.exists(output_path)):
              print(
                  "[skip] n="
                  + str(n)
                  + ": array files not found (run generator.cpp first)"
              )
              continue
          
          source_arr = load_array(input_path)
          expected = load_array(output_path)

          for name, func in algorithms.items():
              result = benchmarking(func, source_arr, expected, TRIALS)
              if not result["correct"]:
                  print(
                      "[ERROR] "
                      + name
                      + " n="
                      + str(n)
                      + ": produced INCORRECT sort check implementation"
                  )
              print(
                  f"{name:<16} {n:>8} {result['time_mean_ms']:>12.3f} "
                  f"{result['comparisons']:>14} {result['writes']:>12} "
                  f"{'ok' if result['correct'] else 'fail':>5}"
              )
              writer.writerow(
                  {
                      "algorithm": name,
                      "n": n,
                      "time_mean_ms": result["time_mean_ms"],
                      "time_std_ms": result["time_std_ms"],
                      "comparisons": result["comparisons"],
                      "writes": result["writes"],
                      "correct": result["correct"],
                  }
              )
              f.flush()
              
  print("\n" + "Results written to " + RESULTS_CSV)

#plotting
def load_results():
    data = {}  # algorithm -> list of row dicts
    
    with open(RESULTS_CSV, newline="") as f:
      for row in csv.DictReader(f):
        data.setdefault(row["algorithm"], []).append(row)
    
    for rows in data.values():
      #r:input parameter passed by .sort() representing single row dict. rows.
      #int(r["n"]): value returned by lambda function.
      #key=: tells .sort(): "Don't sort dict.s directly;sort on int of r["n"].
      rows.sort(key=lambda r: int(r["n"]))
    
    return data

def plot_metric(data, key, ylabel, title, out_name):
  plt.figure(figsize=(8, 6))
  
  for algo, rows in data.items():
    xs = [int(r["n"]) for r in rows]
    ys = [float(r[key]) for r in rows]
    plt.plot(xs, ys, marker="o", label=algo)

  plt.xlabel("Array size (n)")
  plt.ylabel(ylabel)
  plt.title(title)
  plt.legend()
  plt.grid(True, alpha=0.3)
  
  out_path = os.path.join(REPORTS_DIR, out_name)
  plt.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close()
  print(f"Saved {out_path}")

def make_plots():
  data = load_results()
  plot_metric(data, "time_mean_ms", "Time (ms)", "Time vs Array Size", "time_vs_n.png")
  plot_metric(data, "comparisons", "Comparisons", "Comparisons vs Array Size", "comparisons_vs_n.png")
  plot_metric(data, "writes", "Writes", "Writes vs Array Size", "writes_vs_n.png")


if __name__ == "__main__":
    algorithms = discover_algos()
    print("Discovered algorithms: " + str(list(algorithms.keys())) + "\n")
    run_benchmarks(algorithms)
    make_plots()