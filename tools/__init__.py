"""Tools package providing file system and calculation tools for docchat."""
import os


def is_path_safe(path):
    """
    Return True if path is safe: no absolute paths and no directory traversal.

    >>> is_path_safe('.')
    True
    >>> is_path_safe('subdir/file.txt')
    True
    >>> is_path_safe('/etc/passwd')
    False
    >>> is_path_safe('..')
    False
    >>> is_path_safe('../secret')
    False
    >>> is_path_safe('subdir/../other')
    False
    """
    if os.path.isabs(path):
        return False
    parts = path.replace('\\', '/').split('/')
    return '..' not in parts
