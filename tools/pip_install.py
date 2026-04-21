"""pip install tool for the docchat agent."""
import subprocess

SCHEMA = {
    "type": "function",
    "function": {
        "name": "pip_install",
        "description": "Install a Python library using pip.",
        "parameters": {
            "type": "object",
            "properties": {
                "library_name": {
                    "type": "string",
                    "description": "The name of the library to install.",
                }
            },
            "required": ["library_name"],
        },
    },
}


def pip_install(library_name):
    """
    Install a Python library with pip3 and return the output.

    >>> result = pip_install('pip').lower()
    >>> 'successfully installed' in result or 'already satisfied' in result
    True
    """
    result = subprocess.run(
        ['pip3', 'install', library_name],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    return output.strip()
