""""Enums" representing categories of evaluation.

All "enum values" must be specified in alphabetical order.
"""

class Mode:
    """Evaluation mode representing whether student is testing or submitting."""
    submit, test = range(2)

class Stack:
    """Language and testing framework for the quiz."""
    js, js_mocha, rb, swift = range(4)
