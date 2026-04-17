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
