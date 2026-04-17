"""File content reading tool for the docchat agent."""
from tools import is_path_safe

SCHEMA = {
    "type": "function",
    "function": {
        "name": "cat",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The file path to read.",
                }
            },
            "required": ["path"],
        },
    },
}


def cat(path):
    """
    Return the contents of a file as a string, handling encoding errors.

    >>> cat('test_data/hello.txt')
    'Hello, World!'
    >>> cat('test_data/utf16.txt')
    'Hello UTF-16'
    >>> cat('test_data/binary.bin')
    'Error: Unable to decode file: test_data/binary.bin'
    >>> cat('/etc/passwd')
    'Error: path is not safe'
    >>> cat('../secret')
    'Error: path is not safe'
    >>> cat('nonexistent_file_xyz.txt')
    'Error: File not found: nonexistent_file_xyz.txt'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f'Error: File not found: {path}'
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-16') as f:
                return f.read()
        except UnicodeDecodeError:
            return f'Error: Unable to decode file: {path}'
