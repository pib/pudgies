def assignment_expression(context, name, value):
    context[name] = value
    return value
