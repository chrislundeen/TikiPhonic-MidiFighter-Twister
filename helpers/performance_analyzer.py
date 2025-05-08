"""
Performance analysis utilities for MidiFighter Twister Configuration Generator.

This module provides utilities for collecting, analyzing, and visualizing
performance metrics from the different components of the MidiFighter Twister
Configuration Generator.
"""

import time
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import datetime

# Define a class to store and analyze performance metrics
class PerformanceTracker:
    """Track and analyze performance metrics across test runs"""

    def __init__(self, log_dir: str = "performance_logs"):
        """Initialize the performance tracker with a directory for logs

        Args:
            log_dir: Directory to store performance logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        self.current_run_metrics = {}
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def add_metric(self, component: str, metrics: Dict[str, float]) -> None:
        """Add performance metrics for a component

        Args:
            component: Name of the component being measured
            metrics: Dictionary of performance metrics
        """
        self.current_run_metrics[component] = metrics

    def save_metrics(self, run_name: Optional[str] = None) -> str:
        """Save the current metrics to a JSON file

        Args:
            run_name: Optional name for the test run

        Returns:
            Path to the saved metrics file
        """
        if not run_name:
            run_name = f"run_{self.timestamp}"

        # Add timestamp to metrics
        metrics_with_meta = {
            "timestamp": self.timestamp,
            "run_name": run_name,
            "metrics": self.current_run_metrics
        }

        # Save to file
        output_file = self.log_dir / f"{run_name}_{self.timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(metrics_with_meta, f, indent=2)

        return str(output_file)

    def load_previous_runs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Load metrics from previous runs

        Args:
            limit: Maximum number of previous runs to load

        Returns:
            List of metrics from previous runs, sorted by timestamp (newest first)
        """
        metric_files = list(self.log_dir.glob("*.json"))
        metric_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        previous_runs = []
        for file_path in metric_files[:limit]:
            try:
                with open(file_path, 'r') as f:
                    run_data = json.load(f)
                    previous_runs.append(run_data)
            except (json.JSONDecodeError, IOError):
                # Skip invalid files
                continue

        return previous_runs

    def compare_with_previous(self, component: str) -> Dict[str, Any]:
        """Compare current metrics with previous runs for a specific component

        Args:
            component: Name of the component to compare

        Returns:
            Dictionary with comparison results
        """
        previous_runs = self.load_previous_runs()

        if not previous_runs or component not in self.current_run_metrics:
            return {"status": "No previous data available"}

        # Extract metrics for the specified component
        current_metrics = self.current_run_metrics[component]

        # Collect metrics from previous runs
        previous_metrics = []
        for run in previous_runs:
            if "metrics" in run and component in run["metrics"]:
                previous_metrics.append(run["metrics"][component])

        if not previous_metrics:
            return {"status": f"No previous data for component {component}"}

        # Calculate averages from previous runs
        avg_time = sum(m.get("execution_time", 0) for m in previous_metrics) / len(previous_metrics)
        avg_memory = sum(m.get("memory_used", 0) for m in previous_metrics) / len(previous_metrics)

        # Compare with current
        time_diff = current_metrics.get("execution_time", 0) - avg_time
        time_diff_pct = (time_diff / avg_time) * 100 if avg_time else 0

        memory_diff = current_metrics.get("memory_used", 0) - avg_memory
        memory_diff_pct = (memory_diff / avg_memory) * 100 if avg_memory else 0

        return {
            "status": "comparison_available",
            "current": current_metrics,
            "previous_avg": {
                "execution_time": avg_time,
                "memory_used": avg_memory
            },
            "difference": {
                "execution_time": time_diff,
                "execution_time_pct": time_diff_pct,
                "memory_used": memory_diff,
                "memory_used_pct": memory_diff_pct
            }
        }

    def generate_report(self) -> str:
        """Generate a text report summarizing the current metrics

        Returns:
            String containing the report text
        """
        report_lines = ["Performance Metrics Report", "=" * 25, ""]
        report_lines.append(f"Run timestamp: {self.timestamp}")
        report_lines.append("")

        # Add component metrics
        for component, metrics in self.current_run_metrics.items():
            report_lines.append(f"Component: {component}")
            report_lines.append("-" * 15)
            report_lines.append(f"  Execution time: {metrics.get('execution_time', 0):.4f} seconds")
            report_lines.append(f"  Memory used: {metrics.get('memory_used', 0):.2f} MB")

            # Add comparison with previous runs
            comparison = self.compare_with_previous(component)
            if comparison.get("status") == "comparison_available":
                diff = comparison["difference"]
                time_diff = diff["execution_time"]
                time_diff_pct = diff["execution_time_pct"]
                memory_diff = diff["memory_used"]
                memory_diff_pct = diff["memory_used_pct"]

                time_trend = "faster" if time_diff < 0 else "slower"
                memory_trend = "less" if memory_diff < 0 else "more"

                report_lines.append(f"  Comparison to previous runs:")
                report_lines.append(f"    Time: {abs(time_diff_pct):.1f}% {time_trend}")
                report_lines.append(f"    Memory: {abs(memory_diff_pct):.1f}% {memory_trend}")

            report_lines.append("")

        # Generate overall summary
        report_lines.append("Overall Summary")
        report_lines.append("-" * 15)

        # Find component with highest execution time
        if self.current_run_metrics:
            slowest_component = max(
                self.current_run_metrics.items(),
                key=lambda x: x[1].get("execution_time", 0)
            )[0]

            most_memory = max(
                self.current_run_metrics.items(),
                key=lambda x: x[1].get("memory_used", 0)
            )[0]

            report_lines.append(f"Slowest component: {slowest_component}")
            report_lines.append(f"Most memory-intensive component: {most_memory}")

        return "\n".join(report_lines)

# Utility function to record metrics from test runs
def collect_metrics_from_test(test_result: Dict[str, Dict[str, float]], tracker: Optional[PerformanceTracker] = None) -> PerformanceTracker:
    """Collect metrics from a test result and add them to a tracker

    Args:
        test_result: Dictionary containing test results with metrics
        tracker: Optional existing PerformanceTracker instance

    Returns:
        PerformanceTracker with the collected metrics
    """
    if tracker is None:
        tracker = PerformanceTracker()

    for component, metrics in test_result.items():
        tracker.add_metric(component, metrics)

    return tracker

# Main function to run from command line
def main():
    """Main function to generate a performance report"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate performance reports")
    parser.add_argument("--log-dir", default="performance_logs", help="Directory for performance logs")
    parser.add_argument("--report", action="store_true", help="Generate a report from the latest run")
    args = parser.parse_args()

    tracker = PerformanceTracker(log_dir=args.log_dir)

    if args.report:
        # Load the latest run
        previous_runs = tracker.load_previous_runs(limit=1)
        if previous_runs:
            latest_run = previous_runs[0]
            # Reconstruct metrics
            for component, metrics in latest_run.get("metrics", {}).items():
                tracker.add_metric(component, metrics)

            # Generate and print report
            report = tracker.generate_report()
            print(report)
        else:
            print("No previous runs found")
    else:
        print("No action specified. Use --report to generate a report.")

if __name__ == "__main__":
    main()
