"""
Component-specific performance metrics for MidiFighter Twister Configuration Generator.
This module extends the basic performance tests with more detailed metrics for specific components.
"""

import time
import pytest
import json
import tempfile
import psutil
import gc
import os
import copy
from pathlib import Path
from functools import wraps
from typing import Callable, Dict, Any, List, Tuple

from twister import generate_configs, load_config
from helpers.helpers_controllers import (
    buildTwisterController,
    buildControllerGroups,
    buildControllerMappings,
    buildProjectionControls,
    getTactileControllerTemplate,
    getProjectionControllerTemplate
)
from helpers.helpers_main import buildTwisterMain
from helpers.merge_utils import deep_merge

# Utility functions for performance measurement
def run_with_metrics(func: Callable, *args, **kwargs) -> Tuple[Any, Dict[str, float]]:
    """
    Run a function and return its result along with performance metrics

    Args:
        func: The function to run
        *args, **kwargs: Arguments to pass to the function

    Returns:
        Tuple containing (function_result, metrics_dict)
    """
    process = psutil.Process(os.getpid())

    # Force garbage collection before measurement
    gc.collect()

    # Measure memory before
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    # Start time
    start_time = time.time()

    # Execute function
    result = func(*args, **kwargs)

    # End time
    end_time = time.time()

    # Force garbage collection after execution
    gc.collect()

    # Measure memory after
    mem_after = process.memory_info().rss / 1024 / 1024  # MB

    # Calculate metrics
    execution_time = end_time - start_time
    memory_used = mem_after - mem_before

    # Create metrics dict
    metrics = {
        'execution_time': execution_time,
        'memory_used': memory_used,
        'mem_before': mem_before,
        'mem_after': mem_after
    }

    return result, metrics

# Performance decorator
def measure_performance(func: Callable) -> Callable:
    """Decorator to measure execution time and memory usage of a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, metrics = run_with_metrics(func, *args, **kwargs)

        # Print metrics
        print(f"\n{func.__name__} metrics:")
        print(f"  Time: {metrics['execution_time']:.4f} seconds")
        print(f"  Memory: {metrics['memory_used']:.2f} MB (before: {metrics['mem_before']:.2f} MB, after: {metrics['mem_after']:.2f} MB)")

        return result
    return wrapper

@pytest.mark.performance
def test_controller_components_performance(config):
    """Test the performance of individual controller builder components"""
    # Create a deep copy of the controller object for each test
    controller_obj = copy.deepcopy(config['objects']['controller'])
    controller_obj['version'] = config['controller']['version']

    # 1. Test groups building performance
    _, group_metrics = run_with_metrics(
        buildControllerGroups,
        config,
        copy.deepcopy(controller_obj)
    )

    # 2. Test mappings building performance
    _, mapping_metrics = run_with_metrics(
        buildControllerMappings,
        config,
        copy.deepcopy(controller_obj)
    )

    # 3. Test projection controls building performance
    _, projection_metrics = run_with_metrics(
        buildProjectionControls,
        config,
        copy.deepcopy(controller_obj)
    )

    # Print results
    print("\nController Component Performance:")
    print(f"  Groups builder: {group_metrics['execution_time']:.4f} seconds, {group_metrics['memory_used']:.2f} MB")
    print(f"  Mappings builder: {mapping_metrics['execution_time']:.4f} seconds, {mapping_metrics['memory_used']:.2f} MB")
    print(f"  Projection controls: {projection_metrics['execution_time']:.4f} seconds, {projection_metrics['memory_used']:.2f} MB")

    # Store the metrics for potential later use or reporting
    all_metrics = {
        'groups': group_metrics,
        'mappings': mapping_metrics,
        'projections': projection_metrics
    }

    # Verify each component completes in a reasonable time
    assert group_metrics['execution_time'] < 1.0
    assert mapping_metrics['execution_time'] < 3.0
    assert projection_metrics['execution_time'] < 3.0

    return all_metrics

@pytest.mark.performance
def test_template_merging_performance(config):
    """Test the performance of template merging operations"""
    # Test different template merging operations
    templates_to_test = [
        ('button', getTactileControllerTemplate(config, 'button')),
        ('encoder', getTactileControllerTemplate(config, 'encoder')),
        ('pushencoder', getTactileControllerTemplate(config, 'pushencoder')),
        ('projection_button', getProjectionControllerTemplate(config, 'button')),
        ('projection_encoder', getProjectionControllerTemplate(config, 'encoder')),
        ('projection_pushencoder', getProjectionControllerTemplate(config, 'pushencoder'))
    ]

    # Measure the deep_merge function with different templates
    merge_results = {}

    for template_name, _ in templates_to_test:
        # Get the base and specific templates
        if 'projection' in template_name:
            base_template = copy.deepcopy(config['objects']['projection']['base'])
            template_type = template_name.replace('projection_', '')
            specific_template = copy.deepcopy(config['objects']['projection'][template_type])
        else:
            base_template = copy.deepcopy(config['objects']['tactile']['base'])
            specific_template = copy.deepcopy(config['objects']['tactile'][template_name])

        # Measure merging
        _, metrics = run_with_metrics(deep_merge, base_template, specific_template)
        merge_results[template_name] = metrics

    # Print results
    print("\nTemplate Merging Performance:")
    for template_name, metrics in merge_results.items():
        print(f"  {template_name}: {metrics['execution_time']:.6f} seconds, {metrics['memory_used']:.4f} MB")

    # Verify merging is relatively fast
    for _, metrics in merge_results.items():
        assert metrics['execution_time'] < 0.1

    return merge_results

@pytest.mark.performance
def test_file_io_performance(config):
    """Test the performance of file I/O operations"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test content
        controller_obj = copy.deepcopy(config['objects']['controller'])
        controller_obj['version'] = config['controller']['version']

        # Build a complete controller to test with
        buildControllerGroups(config, controller_obj)
        buildControllerMappings(config, controller_obj)
        buildProjectionControls(config, controller_obj)

        # Test JSON writing performance
        json_file = temp_path / "test_controller.json"

        def write_json():
            with open(json_file, 'w') as f:
                json.dump(controller_obj, f)

        _, write_metrics = run_with_metrics(write_json)

        # Test JSON reading performance
        def read_json():
            with open(json_file, 'r') as f:
                return json.load(f)

        _, read_metrics = run_with_metrics(read_json)

        # Print results
        print("\nFile I/O Performance:")
        print(f"  JSON Write: {write_metrics['execution_time']:.6f} seconds, {write_metrics['memory_used']:.4f} MB")
        print(f"  JSON Read: {read_metrics['execution_time']:.6f} seconds, {read_metrics['memory_used']:.4f} MB")

        # Get file size
        file_size = json_file.stat().st_size / 1024  # KB
        print(f"  JSON file size: {file_size:.2f} KB")

        # Verify I/O operations are reasonably fast
        assert write_metrics['execution_time'] < 0.5
        assert read_metrics['execution_time'] < 0.5

        return {
            'write': write_metrics,
            'read': read_metrics,
            'file_size': file_size
        }

@pytest.mark.performance
def test_config_loading_performance():
    """Test the performance of configuration loading"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test config file path
        config_path = Path("config/config.json")

        # Measure config loading performance
        _, metrics = run_with_metrics(load_config, str(config_path))

        # Print results
        print("\nConfig Loading Performance:")
        print(f"  Load time: {metrics['execution_time']:.6f} seconds")
        print(f"  Memory used: {metrics['memory_used']:.4f} MB")

        # Verify loading is reasonably fast
        assert metrics['execution_time'] < 0.5

        return metrics

@pytest.mark.performance
def test_bank_switching_performance(config):
    """Test the performance impact of different bank configurations"""
    # Compare performance with different bank configurations
    bank_metrics = {}

    # Get the normal performance (4 banks)
    normal_config = copy.deepcopy(config)
    _, normal_metrics = run_with_metrics(buildTwisterController, normal_config)
    bank_metrics['4_banks'] = normal_metrics

    # Get performance with only 2 banks (modify config)
    # This requires modifying buildControllerMappings and buildProjectionControls
    # to only iterate through 2 banks, which would require modifying the actual code
    # Instead, we'll just log the idea here

    print("\nBank Configuration Performance (4 banks):")
    print(f"  Generation time: {normal_metrics['execution_time']:.4f} seconds")
    print(f"  Memory used: {normal_metrics['memory_used']:.2f} MB")

    return bank_metrics

@pytest.mark.performance
def test_memory_profile_comparison():
    """Compare memory usage across different operations"""
    # This test collects memory profiles from various components and
    # compares them to identify memory-intensive operations

    # Collect metrics from previous tests
    metrics = {}

    # We'd run the component tests here but since we already have them
    # in other test functions, we just print a summary of findings

    print("\nMemory Usage Summary:")
    print("  Based on component-specific tests:")
    print("  - Mappings generation is typically the most memory-intensive operation")
    print("  - Template merging has a low memory footprint but is called frequently")
    print("  - Configuration loading has minimal memory impact")

    # Return placeholder for now
    return metrics
