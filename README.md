What is it?
===========

Pudgies (kind of how you'd pronounce pyjs) is a JavaScript-to-Python
compiler and runtime library.

It currently is in very early stages of development, only supporing
very basic assignments of strings and numbers.

The eventual goal is to be able to compile .js files to .pyc files
which will be importable from within other python modules. These js
modules will able to be used either just like any other Python module,
or sandboxed from the rest of the Python world for safe execution of
untrusted scripts.

At the moment, there are functions to take a string of JavaScript and
get either a Python AST or a Python Module object. In future versions,
the ability to save modules to .pyc files will be added.


How does it work?
=================

Pudgies works by parsing JavaScript into an abstract syntax tree (via
the [pynarcissus JavaScript
parser](http://code.google.com/p/pynarcissus/)), and then that AST is
translated into a [Python
AST](http://docs.python.org/library/ast.html#module-ast), which is
then compiled using Python's built-in [compile
function](http://docs.python.org/library/functions.html#compile).

The resulting code object can then either be executed within the
context of a new module to create a usable module, or written out to a
.pyc file, which can then be imported via Python's built-in import
functionality.