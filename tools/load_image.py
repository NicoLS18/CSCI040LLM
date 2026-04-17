"""Tool for loading a local image into the chat message history."""
import base64
import mimetypes
import os

SCHEMA = {
    "type": "function",
    "function": {
        "name": "load_image",
        "description": "Load a local image file so the LLM can see it.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the image file (JPEG, PNG, GIF, or WebP).",
                }
            },
            "required": ["path"],
        },
    },
}


# this was a good use of "memory management" tricks to pass in messages
# here and then modify it in the function;
# this is almost as clean of a way to implement this ec as possible;
# nicley done!
def load_image(path, messages):
    """
    Load a local image file and inject it into the messages list as a
    vision-compatible user message.  Returns a confirmation string.

    Because tool results must be plain text, this function directly appends
    to the shared messages list rather than returning the image data.

    >>> msgs = []
    >>> load_image('test_data/test.png', msgs)
    'Image loaded: test_data/test.png'
    >>> msgs[0]['role']
    'user'
    >>> load_image('nonexistent_xyz.png', [])
    'Error: file not found: nonexistent_xyz.png'
    >>> load_image('test_data/hello.txt', [])
    'Error: unsupported image type: text/plain'
    """
    if not os.path.isfile(path):
        return f'Error: file not found: {path}'
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type not in ('image/jpeg', 'image/png', 'image/gif', 'image/webp'):
        return f'Error: unsupported image type: {mime_type}'
    with open(path, 'rb') as f:
        data = base64.standard_b64encode(f.read()).decode('utf-8')
    messages.append({
        'role': 'user',
        'content': [
            {
                'type': 'image_url',
                'image_url': {
                    'url': f'data:{mime_type};base64,{data}',
                },
            }
        ],
    })
    return f'Image loaded: {path}'
