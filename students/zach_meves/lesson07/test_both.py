"""
Tests both linear and parallel modules using exec_tests.py.

Run as `python test_both.py`.
"""

import subprocess

# Run linear tests
print("Running linear tests", flush=True)
subprocess.run("python -m unittest exec_tests.py linear")

print("Running parallel tests", flush=True)
subprocess.run("python -m unittest exec_tests.py parallel")
