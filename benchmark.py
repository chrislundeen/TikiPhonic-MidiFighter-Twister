#!/usr/bin/env python
"""
Simple benchmark script for the MidiFighter Twister Configuration Generator.
Measures performance of key operations.
"""

import time
import json
import os
import sys
import gc
import psutil
from pathlib import Path

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.abspath('.'))

try:
    from twister import generate_configs

    def benchmark_function(func, *args, **kwargs):
        """Measure execution time and memory usage of a function"""
        print(f"Starting benchmark of {func.__name__}...")
        process = psutil.Process(os.getpid())

        # Force garbage collection to get more accurate memory measurements
        gc.collect()

        # Measure memory before
        mem_before = process.memory_info().rss / (1024 * 1024)  # MB

        # Measure execution time
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Record end time
        execution_time = time.time() - start_time

        # Force garbage collection again before measuring final memory
        gc.collect()

        # Measure memory after
        mem_after = process.memory_info().rss / (1024 * 1024)  # MB
        memory_used = mem_after - mem_before

        print(f"Finished benchmark of {func.__name__}")

        return {
            "execution_time": execution_time,
            "memory_used": memory_used,
            "mem_before": mem_before,
            "mem_after": mem_after
        }

    def save_benchmark_results(results, name="benchmark", output_dir="performance_logs"):
        """Save benchmark results to a JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{name}_{timestamp}.json")

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        return output_path

    def run_config_generation_benchmark():
        """Run benchmark for config generation"""
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        # Run benchmark
        metrics = benchmark_function(generate_configs)

        # Save results
        results = {
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
            "metrics": {
                "config_generation": metrics
            }
        }

        output_path = save_benchmark_results(results, "config_generation")

        # Print results
        print(f"\nBenchmark Results:")
        print(f"  Execution time: {metrics['execution_time']:.6f} seconds")
        print(f"  Memory used: {metrics['memory_used']:.2f} MB")
        print(f"  Results saved to: {output_path}")

    if __name__ == "__main__":
        print("Running MidiFighter Twister configuration generation benchmark...")
        run_config_generation_benchmark()

except Exception as e:
    print(f"Error running benchmark: {e}")
    import traceback
    traceback.print_exc()
