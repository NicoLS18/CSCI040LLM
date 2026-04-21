"""Multi-file writing tool with a single git commit for the docchat agent."""
import subprocess
from tools import is_path_safe
from tools.write_file import _apply_diff

SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": (
            "Write or patch multiple files and commit them all in a single git commit. "
            "Each file entry must have 'path' and either 'contents' or 'diff'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "description": "List of objects with 'path' and either 'contents' or 'diff'.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "contents": {"type": "string"},
                            "diff": {"type": "string"},
                        },
                        "required": ["path"],
                    },
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message (prefixed with [docchat]).",
                },
            },
            "required": ["files", "commit_message"],
        },
    },
}


def write_files(files, commit_message):
    """
    Write or patch each file in the list and create one git commit for all.

    Each entry needs 'path' and either 'contents' or 'diff'.
    Returns an error string if any path is unsafe, without writing anything.

    >>> write_files([{'path': '/etc/passwd', 'contents': 'x'}], 'bad')
    'Error: path is not safe: /etc/passwd'
    >>> write_files([{'path': '../evil.txt', 'contents': 'x'}], 'bad')
    'Error: path is not safe: ../evil.txt'
    >>> write_files([{'path': 'test_data/hello.txt'}], 'bad')
    'Error: provide either contents or diff for test_data/hello.txt'
    """
    for entry in files:
        if not is_path_safe(entry['path']):
            return f"Error: path is not safe: {entry['path']}"
        if 'contents' not in entry and 'diff' not in entry:
            return f"Error: provide either contents or diff for {entry['path']}"
    written = []
    for entry in files:
        path = entry['path']
        if 'diff' in entry:
            error = _apply_diff(path, entry['diff'])
            if error:
                return error
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(entry['contents'])
        subprocess.run(['git', 'add', path], check=True)
        written.append(path)
    subprocess.run(
        ['git', 'commit', '-m', f'[docchat] {commit_message}'],
        check=True,
    )
    return f"Written and committed: {', '.join(written)}"
