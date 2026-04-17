"""Regex-based file search tool for the docchat agent."""
import re
import glob as glob_module
from tools import is_path_safe

SCHEMA = {
    "type": "function",
    "function": {
        "name": "grep",
        "description": "Search for lines matching a regex pattern in files.",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The regex pattern to search for.",
                },
                "path": {
                    "type": "string",
                    "description": "File path or glob pattern to search.",
                },
            },
            "required": ["pattern", "path"],
        },
    },
}


def grep(pattern, path):
    """
    Search files matching a glob path for lines matching a regex pattern.

    >>> grep('Hello', 'test_data/hello.txt')
    'Hello, World!'
    >>> grep('number', 'test_data/numbers.txt')
    'number1\\nnumber2\\nnumber3'
    >>> grep('xyz_no_match', 'test_data/hello.txt')
    ''
    >>> grep('Hello', 'test_data/binary.bin')
    ''
    >>> grep('Hello', '/etc/passwd')
    'Error: path is not safe'
    >>> grep('Hello', '../secret')
    'Error: path is not safe'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    files = glob_module.glob(path)
    matches = []
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if re.search(pattern, line):
                        matches.append(line.rstrip('\n'))
        except (FileNotFoundError, UnicodeDecodeError):
            pass
    return '\n'.join(matches)
