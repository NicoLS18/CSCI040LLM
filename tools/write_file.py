"""File writing tool with git commit support for the docchat agent."""
import subprocess
from tools import is_path_safe
from tools.doctests import doctests

SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Write contents to a file, commit it to git, "
            "and run doctests if it is a Python file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to write.",
                },
                "contents": {
                    "type": "string",
                    "description": "Text content to write into the file.",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message (prefixed with [docchat]).",
                },
            },
            "required": ["path", "contents", "commit_message"],
        },
    },
}


def write_file(path, contents, commit_message):
    """
    Write contents to path, git-add and commit, then run doctests if Python.

    >>> write_file('/etc/passwd', 'x', 'bad')
    'Error: path is not safe'
    >>> write_file('../evil.txt', 'x', 'bad')
    'Error: path is not safe'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contents)
    subprocess.run(['git', 'add', path], check=True)
    subprocess.run(
        ['git', 'commit', '-m', f'[docchat] {commit_message}'],
        check=True,
    )
    if path.endswith('.py'):
        return doctests(path)
    return f'Written and committed: {path}'
