"""File writing tool with git commit support for the docchat agent."""
import subprocess
import tempfile
import os
from tools import is_path_safe
from tools.doctests import doctests

SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Write or patch a file, commit it to git, "
            "and run doctests if it is a Python file. "
            "Provide either 'contents' to overwrite the file or 'diff' to patch it."
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
                    "description": "Full text to write (mutually exclusive with diff).",
                },
                "diff": {
                    "type": "string",
                    "description": "Unified diff to apply to the file (exclusive with contents).",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message (prefixed with [docchat]).",
                },
            },
            "required": ["path", "commit_message"],
        },
    },
}


def _apply_diff(path, diff_text):
    """
    Apply a unified diff to path using `patch --fuzz 10`.
    Returns None on success or an error string on failure.

    >>> _apply_diff('/etc/passwd', 'x')
    'Error: path is not safe'
    >>> _apply_diff('../evil.txt', 'x')
    'Error: path is not safe'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as tmp:
        tmp.write(diff_text)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ['patch', '--fuzz', '10', path, tmp_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f'Error applying diff: {result.stderr.strip() or result.stdout.strip()}'
        return None
    finally:
        os.unlink(tmp_path)


def write_file(path, commit_message, contents=None, diff=None):
    """
    Write or patch a file, git-add and commit, then run doctests if Python.

    Exactly one of contents or diff must be provided.

    >>> write_file('/etc/passwd', 'bad', contents='x')
    'Error: path is not safe'
    >>> write_file('../evil.txt', 'bad', contents='x')
    'Error: path is not safe'
    >>> write_file('test_data/hello.txt', 'bad')
    'Error: provide either contents or diff, not neither'
    >>> write_file('test_data/hello.txt', 'bad', contents='a', diff='b')
    'Error: provide either contents or diff, not both'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    if contents is None and diff is None:
        return 'Error: provide either contents or diff, not neither'
    if contents is not None and diff is not None:
        return 'Error: provide either contents or diff, not both'
    if diff is not None:
        error = _apply_diff(path, diff)
        if error:
            return error
    else:
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
