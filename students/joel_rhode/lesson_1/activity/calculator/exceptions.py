"""This module handles exceptions for the calculator."""


class InsufficientOperands(Exception):
    """Handles exceptions for too few operands are present at calculation."""
    print("Too few operands, input number into stack before calculating.")
