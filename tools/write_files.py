"""Multi-file writing tool with a single git commit for the docchat agent."""
import subprocess
from tools import is_path_safe

SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": (
            "Write multiple files and commit them all in a single git commit."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "description": "List of objects with 'path' and 'contents' keys.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "contents": {"type": "string"},
                        },
                        "required": ["path", "contents"],
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
    Write each file in the list and create one git commit for all of them.

    Each item in files must be a dict with 'path' and 'contents' keys.
    Returns an error string if any path is unsafe, without writing anything.

    >>> write_files([{'path': '/etc/passwd', 'contents': 'x'}], 'bad')
    'Error: path is not safe: /etc/passwd'
    >>> write_files([{'path': '../evil.txt', 'contents': 'x'}], 'bad')
    'Error: path is not safe: ../evil.txt'
    """
    for entry in files:
        if not is_path_safe(entry['path']):
            return f"Error: path is not safe: {entry['path']}"
    written = []
    for entry in files:
        with open(entry['path'], 'w', encoding='utf-8') as f:
            f.write(entry['contents'])
        subprocess.run(['git', 'add', entry['path']], check=True)
        written.append(entry['path'])
    subprocess.run(
        ['git', 'commit', '-m', f'[docchat] {commit_message}'],
        check=True,
    )
    return f"Written and committed: {', '.join(written)}"
