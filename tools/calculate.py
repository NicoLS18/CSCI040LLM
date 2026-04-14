"""Arithmetic calculation tool for the docchat agent."""


def calculate(expression):
    """
    Evaluate a mathematical expression and return the result as a string.

    >>> calculate('2 + 2')
    '4'
    >>> calculate('10 * 5 - 3')
    '47'
    >>> calculate('2 ** 8')
    '256'
    >>> calculate('9 / 2')
    '4.5'
    """
    result = eval(expression)
    return str(result)
