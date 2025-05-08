#!/usr/bin/env python
"""
Run performance tests and generate a comprehensive report for the MidiFighter Twister Configuration Generator.

Usage:
    python run_performance_tests.py [--save-logs]

Options:
    --save-logs    Save detailed logs for each component
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

try:
    from helpers.performance_analyzer import PerformanceTracker
except ImportError:
    print("Performance analyzer not found. Please run this script from the project root.")
    sys.exit(1)

def run_performance_tests(save_logs=False):
    """Run all performance tests and collect results"""
    print("Running performance tests...")

    # Run pytest with the performance mark
    cmd = ["pytest", "-v", "-m", "performance"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    print("\nTest Output:")
    print(result.stdout)

    if result.returncode != 0:
        print("\nError running tests:")
        print(result.stderr)
        return False

    # Check if logs directory exists
    logs_dir = Path("performance_logs")
    if logs_dir.exists():
        # Get the most recent log file
        log_files = list(logs_dir.glob("*.json"))
        if log_files:
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            latest_log = log_files[0]

            # Create a tracker and load the log
            tracker = PerformanceTracker()
            previous_runs = tracker.load_previous_runs(limit=1)

            if previous_runs:
                # Generate report
                report = tracker.generate_report()

                # Save report to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = logs_dir / f"performance_report_{timestamp}.txt"
                with open(report_file, 'w') as f:
                    f.write(report)

                print(f"\nPerformance report saved to {report_file}")

                # Print summary
                print("\nPerformance Summary:")
                print(report)

                return True

    print("No performance logs found.")
    return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run performance tests for MidiFighter Twister")
    parser.add_argument("--save-logs", action="store_true", help="Save detailed logs")
    args = parser.parse_args()

    # Create logs directory
    logs_dir = Path("performance_logs")
    logs_dir.mkdir(exist_ok=True)

    # Run tests
    success = run_performance_tests(save_logs=args.save_logs)

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
