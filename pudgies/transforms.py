import ast
import jsparser

ctx = {
    'store': ast.Store(),
    'load': ast.Load(),
    'del': ast.Del(),
}


def dump(tree):
    "utility function to print a textual version of an ast node"
    print ast.dump(tree, annotate_fields=False)

table = {}


def transform(node):
    try:
        trans = table[node.type]
    except KeyError:
        raise SyntaxError('Unknown node type %s' % node.type)
    return trans(node)


def transform_SCRIPT(node):
    statements = []
    for statement in node:
        statements.extend(transform(statement))
    return ast.Module(statements)
table['SCRIPT'] = transform_SCRIPT


def transform_VAR(node):
    assignments = []
    for assign in node:
        name = ast.Name(assign.value, ctx['store'], lineno=assign.lineno,
                        col_offset=assign.start)
        value = transform(assign.initializer)
        assignments.append(ast.Assign([name], value,
                      lineno=assign.lineno, col_offset=assign.start))
    return assignments
table['VAR'] = transform_VAR


def transform_ASSIGN(node):
    return ast.Call(
        ast.Attribute(ast.Name('jslib', ctx['load'], lineno=node.lineno,
                               col_offset=node.start),
                      'assignment_expression', ctx['load'], lineno=node.lineno,
                      col_offset=node.start),
        [ast.Call(ast.Name('locals', ctx['load'], lineno=node.lineno,
                           col_offset=node.start), [], [], None, None,
                  lineno=node.lineno, col_offset=node.start),
         ast.Str(node[0].value, lineno=node[0].lineno,
                 col_offset=node[0].start),
         transform(node[1])], [], None, None, lineno=node.lineno,
        col_offset=node.start)
table['ASSIGN'] = transform_ASSIGN


def transform_STRING(node):
    return ast.Str(node.value, lineno=node.lineno, col_offset=node.start)
table['STRING'] = transform_STRING


def transform_NUMBER(node):
    return ast.Num(node.value, lineno=node.lineno, col_offset=node.start)
table['NUMBER'] = transform_NUMBER


def js_to_ast(source):
    parsetree = jsparser.parse(source)
    tree = transform(parsetree)
    return tree
