"""Doctest runner tool for the docchat agent."""
import subprocess
from tools import is_path_safe

SCHEMA = {
    "type": "function",
    "function": {
        "name": "doctests",
        "description": "Run doctests on a Python file and return the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the Python file to run doctests on.",
                }
            },
            "required": ["path"],
        },
    },
}


def doctests(path):
    """
    Run doctests on a Python file with --verbose and return combined output.

    >>> doctests('/etc/passwd')
    'Error: path is not safe'
    >>> doctests('../secret.py')
    'Error: path is not safe'
    >>> doctests('nonexistent_xyz.py')  # doctest: +ELLIPSIS
    '...'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    result = subprocess.run(
        ['python', '-m', 'doctest', path, '--verbose'],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    return output.strip()
