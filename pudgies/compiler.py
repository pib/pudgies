import imp
from transforms import js_to_ast


def ast_to_mod(name, tree, filename='<string>'):
    code = compile(tree, filename, 'exec')
    mod = imp.new_module(name)
    mod.__file__ = filename
    exec code in globals(), mod.__dict__
    return mod


def compile_mod(name, source, filename='<string>'):
    tree = js_to_ast(source)
    return ast_to_mod(name, tree, filename)
