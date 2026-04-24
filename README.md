# CSCI040LLM

[![Run Tests](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/tests.yml/badge.svg)](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/tests.yml)
[![Integration Test](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/integration.yml/badge.svg)](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/integration.yml)
[![flake8](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/flake8.yml/badge.svg)](https://github.com/NicoLS18/CSCI040LLM/actions/workflows/flake8.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci005-nicolaslaub)](https://pypi.org/project/cmc-csci005-nicolaslaub/)
[![codecov](https://codecov.io/gh/NicoLS18/CSCI040LLM/branch/master/graph/badge.svg)](https://codecov.io/gh/NicoLS18/CSCI040LLM)

A pirate-themed document chat agent powered by the Groq LLM API. Chat naturally with files in your project using tools to list directories, read files, search with regex, and perform calculations.

## Demo Video

The following video demonstrates the Text to Speech capabilites of the agent using an example that also shows its ls tool.
[![Video](https://img.youtube.com/vi/w6ZYI5ZImSQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=w6ZYI5ZImSQ)



This example shows the agent reading files from an eBay scraper project, demonstrating how it can answer questions about unfamiliar codebases and use `/cat` to display file contents.

```
chat> what files are in the ebay scraper project?
Arrr, the ebay scraper project be havin' these files: ebay-dl.py, lego.csv, lego.json, nike shoes.csv, nike shoes.json, README.md, vintage watch.csv, vintage watch.json!

chat> /cat test_projects/ebayscraper/README.md
# ebayscraper
...
```

This example shows the agent searching HTML files with `/grep`, useful for quickly locating specific tags or content across a web project.

```
chat> what html files does the webpage project have?
Arrr, the webpage project be havin' these HTML files: animals.html, index.html, quiz1.html, visit.html, matey!

chat> /grep <title> test_projects/webpage/index.html
<title>Zoo</title>
```

This example shows the agent explaining a project's configuration by reading its `pyproject.toml`, then using `/ls` to explore the package structure.

```
chat> what does the markdown compiler's pyproject.toml say?
Arrr, the pyproject.toml be definin' the project name, version, dependencies, and entry point for the markdown compiler package, matey!

chat> /ls test_projects/markdown-compiler/markdown_compiler
```

## Agent File Creation Example

This example shows the agent creating a new Python file, committing it to git, and running its doctests automatically.

```
chat> create a file called greet.py that has a function greet(name) returning 'Hello, <name>!' with a doctest
[tool] /write_file greet.py ...
Trying:
    greet('Alice')
Expecting:
    'Hello, Alice!'
ok
1 items passed all tests:
  1 tests in greet.greet
1 passed and 0 failed.
Arrr, I've written greet.py with a greet() function and all doctests be passin', matey!

chat> /ls .
...
greet.py
...

$ git log --oneline -3
a1b2c3d [docchat] add greet function with doctest
...

$ cat greet.py
def greet(name):
    """
    Return a greeting string.

    >>> greet('Alice')
    'Hello, Alice!'
    """
    return f'Hello, {name}!'
```

## Agent File Modification Example

This example shows the agent updating an existing file, committing the change, and running doctests automatically.

```
chat> update greet.py so the greet function also accepts an optional exclamation mark
[tool] /write_file greet.py ...
Trying:
    greet('Alice')
Expecting:
    'Hello, Alice!'
ok
Trying:
    greet('Alice', excited=True)
Expecting:
    'Hello, Alice!!'
ok
2 items passed all tests:
  2 tests in greet.greet
2 passed and 0 failed.
Arrr, greet.py has been updated and all doctests be passin', matey!

$ git log --oneline -2
d4e5f6a [docchat] add excited parameter to greet function
a1b2c3d [docchat] add greet function with doctest
```

## Agent File Deletion Example

This example shows the agent removing a file and committing the deletion.

```
chat> delete greet.py since we no longer need it
[tool] /rm greet.py
Removed and committed: greet.py
Arrr, greet.py has been sent to Davy Jones' locker and the deed be committed to git, matey!

$ git log --oneline -2
b2c3d4e [docchat] rm greet.py
a1b2c3d [docchat] add greet function with doctest
```

## Agent Multi-File Creation Example

This example shows the agent writing multiple files in a single git commit.

```
chat> create two files: hello.txt with "Hello World" and bye.txt with "Goodbye World", commit as "add greeting files"
[tool] /write_files ...
Written and committed: hello.txt, bye.txt
Arrr, both files be written and committed in one fell swoop, matey!

$ git log --oneline -1
c3d4e5f [docchat] add greeting files

$ cat hello.txt
Hello World

$ cat bye.txt
Goodbye World
```
