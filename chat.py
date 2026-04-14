"""Docchat: a document-aware AI agent chatbot powered by the Groq LLM API."""
import json
from groq import Groq
from dotenv import load_dotenv
import tools.calculate
import tools.ls
import tools.cat
import tools.grep

load_dotenv()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list (default '.').",
                    }
                },
                "required": [],
            },
        },
    },
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search for lines matching a regex pattern in files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The regex pattern to search for.",
                    },
                    "path": {
                        "type": "string",
                        "description": "File path or glob pattern to search.",
                    },
                },
                "required": ["pattern", "path"],
            },
        },
    },
]


def _execute_tool(name, args):
    """
    Execute a named tool with the given arguments dict and return the result.

    >>> _execute_tool('calculate', {'expression': '2 + 2'})
    '4'
    >>> _execute_tool('ls', {'path': 'test_data'})
    'binary.bin\\nhello.txt\\nnumbers.txt\\nutf16.txt'
    >>> _execute_tool('cat', {'path': 'test_data/hello.txt'})
    'Hello, World!'
    >>> _execute_tool('grep', {'pattern': 'Hello', 'path': 'test_data/hello.txt'})
    'Hello, World!'
    >>> _execute_tool('ls', {})  # doctest: +ELLIPSIS
    '...'
    >>> _execute_tool('unknown', {})
    'Error: unknown tool unknown'
    """
    if name == 'calculate':
        return tools.calculate.calculate(args['expression'])
    elif name == 'ls':
        return tools.ls.ls(args.get('path', '.'))
    elif name == 'cat':
        return tools.cat.cat(args['path'])
    elif name == 'grep':
        return tools.grep.grep(args['pattern'], args['path'])
    return f'Error: unknown tool {name}'


class Chat:
    '''
    An AI chat agent powered by the Groq LLM API that maintains conversation
    history and can invoke tools to explore files and perform calculations.
    Responds in a pirate-themed style.

    >>> chat = Chat()
    >>> chat.send_message('my name is bob', temperature=0.0)
    "Arrr, I be knowin' yer name be Bob, but I don't be havin' any information about ye. What be bringin' ye to these fair waters?"
    >>> chat.send_message('what is my name?', temperature=0.0)
    'Yer name be Bob, matey.'

    >>> chat2 = Chat()
    >>> chat2.send_message('what is my name?', temperature=0.0)
    "I be needin' a bit more information about ye, matey. What be yer name?"
    '''

    def __init__(self):
        """Initialize the chat agent with a pirate-themed system prompt."""
        self.client = Groq()
        self.messages = [
            {
                "role": "system",
                "content": "Write the output in 1-2 sentences. Talk like pirate.",
            }
        ]

    def send_message(self, message, temperature=0.8):
        """
        Send a message and return the response, executing any tool calls first.
        """
        self.messages.append({'role': 'user', 'content': message})
        while True:
            completion = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.1-8b-instant",
                temperature=temperature,
                tools=TOOLS,
            )
            choice = completion.choices[0]
            if choice.finish_reason == 'tool_calls':
                self.messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    name = tool_call.function.name
                    call_args = json.loads(tool_call.function.arguments)
                    result = _execute_tool(name, call_args)
                    self.messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': result,
                    })
            else:
                result = choice.message.content
                self.messages.append(
                    {'role': 'assistant', 'content': result}
                )
                return result


def _handle_slash_command(user_input):
    """
    Parse and execute a slash command, returning the result as a string.

    >>> _handle_slash_command('/ls test_data')
    'binary.bin\\nhello.txt\\nnumbers.txt\\nutf16.txt'
    >>> _handle_slash_command('/cat test_data/hello.txt')
    'Hello, World!'
    >>> _handle_slash_command('/calculate 6 * 7')
    '42'
    >>> _handle_slash_command('/grep Hello test_data/hello.txt')
    'Hello, World!'
    >>> _handle_slash_command('/cat')
    'Error: cat requires a file path'
    >>> _handle_slash_command('/grep Hello')
    'Error: grep requires a pattern and file path'
    >>> _handle_slash_command('/unknown arg')
    'Error: unknown command unknown'
    """
    parts = user_input[1:].split()
    if not parts:
        return 'Error: empty command'
    cmd = parts[0]
    args = parts[1:]
    if cmd == 'calculate':
        return tools.calculate.calculate(' '.join(args))
    elif cmd == 'ls':
        return tools.ls.ls(args[0] if args else '.')
    elif cmd == 'cat':
        if not args:
            return 'Error: cat requires a file path'
        return tools.cat.cat(args[0])
    elif cmd == 'grep':
        if len(args) < 2:
            return 'Error: grep requires a pattern and file path'
        return tools.grep.grep(args[0], args[1])
    return f'Error: unknown command {cmd}'


def repl(temperature=0.8):
    """
    Run the interactive REPL supporting slash commands and LLM chat.

    #monkey patch doctest
    >>> def monkey_input(prompt, user_inputs=['/cat test_data/hello.txt', '/calculate 6 * 7']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl(temperature=0.0)
    chat> /cat test_data/hello.txt
    Hello, World!
    chat> /calculate 6 * 7
    42
    <BLANKLINE>
    """
    try:
        import readline  # noqa: F401
    except ImportError:
        pass
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                print(_handle_slash_command(user_input))
            else:
                response = chat.send_message(user_input, temperature=temperature)
                print(response)
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
