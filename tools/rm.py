"""File removal tool with git commit support for the docchat agent."""
import glob as glob_module
import os
import subprocess
from tools import is_path_safe

SCHEMA = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": "Delete a file (or files matching a glob pattern) and commit the removal.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path or glob pattern to delete.",
                }
            },
            "required": ["path"],
        },
    },
}


def rm(path):
    """
    Delete file(s) matching path/glob and create a git commit.

    >>> rm('/etc/passwd')
    'Error: path is not safe'
    >>> rm('../secret.txt')
    'Error: path is not safe'
    >>> rm('nonexistent_xyz_file.txt')
    'Error: no files found matching nonexistent_xyz_file.txt'
    """
    if not is_path_safe(path):
        return 'Error: path is not safe'
    matches = glob_module.glob(path)
    if not matches:
        return f'Error: no files found matching {path}'
    for filepath in matches:
        os.remove(filepath)
        subprocess.run(['git', 'rm', '--cached', '--ignore-unmatch', filepath])
    subprocess.run(
        ['git', 'commit', '-m', f'[docchat] rm {path}'],
        check=True,
    )
    removed = ', '.join(matches)
    return f'Removed and committed: {removed}'
