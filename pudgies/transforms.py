import ast
import jsparser


def dump(tree):
    "utility function to print a textual version of an ast node"
    print ast.dump(tree, annotate_fields=False)

table = {}


def transform(node, ctx):
    try:
        trans = table[node.type]
    except KeyError:
        raise SyntaxError('Unknown node type %s' % node.type)
    return trans(node, ctx)


def transform_SCRIPT(node, ctx):
    statements = []
    for statement in node:
        statements.extend(transform(statement, ctx))
    return ast.Module(statements)
table['SCRIPT'] = transform_SCRIPT


def transform_VAR(node, ctx):
    assignments = []
    for assign in node:
        name = ast.Name(assign.value, ctx, lineno=assign.lineno,
                        col_offset=assign.start)
        value = transform(assign.initializer, ctx)
        assignments.append(ast.Assign([name], value,
                      lineno=assign.lineno, col_offset=assign.start))
    return assignments
table['VAR'] = transform_VAR


def transform_ASSIGN(node, ctx):
    """
    Aw crap, assignment is an expression on JS, but a statement in Python!
    I predict that this will be a pain in the ass.
    """
table['ASSIGN'] = transform_ASSIGN


def transform_STRING(node, ctx):
    return ast.Str(node.value, lineno=node.lineno, col_offset=node.start)
table['STRING'] = transform_STRING


def transform_NUMBER(node, ctx):
    return ast.Num(node.value, lineno=node.lineno, col_offset=node.start)
table['NUMBER'] = transform_NUMBER


def js_to_ast(source):
    parsetree = jsparser.parse(source)
    context = ast.Store()
    tree = transform(parsetree, context)
    return tree
