"""Arithmetic calculation tool for the docchat agent."""

SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate.",
                }
            },
            "required": ["expression"],
        },
    },
}


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
