"""Tool for loading a local image into the chat message history."""
import base64
import mimetypes
import os


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

    # your doctests here are not great;
    # I understand what they are doing,
    # and I also understand the png file format enought to understand what
    # b'\\x89PNG\\r\\n\\x1a\\n' + b'\\x00' * 8 means,
    # but these tests are not at all obvious the way that tests should be;
    # Better would have been to put a png/jpg/etc file in the test_data
    # folder that you already have and make the test
    # of the same form as your ls/cat/grep tests;
    # for now, I'm not awarding the extra credit,
    # but you can get the ec on the next project by fixing these tests
    # on the project04
    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    >>> _ = tmp.write(b'\\x89PNG\\r\\n\\x1a\\n' + b'\\x00' * 8)
    >>> tmp.close()
    >>> msgs = []
    >>> result = load_image(tmp.name, msgs)
    >>> result.startswith('Image loaded:')
    True
    >>> len(msgs) == 1
    True
    >>> msgs[0]['role']
    'user'
    >>> os.unlink(tmp.name)
    >>> load_image('nonexistent_xyz.png', [])
    'Error: file not found: nonexistent_xyz.png'
    >>> tmp2 = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
    >>> tmp2.close()
    >>> load_image(tmp2.name, [])
    'Error: unsupported image type: text/plain'
    >>> os.unlink(tmp2.name)
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
