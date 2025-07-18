import sys
import os

"""
This package is used in examples for insert the src directory into sys.path.
"""
sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../src")))
