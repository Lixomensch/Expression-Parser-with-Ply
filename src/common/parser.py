"""Modulo parser."""

import math

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611

env = {}
functions = {}

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "POWER"),
    ("right", "UMINUS"),
)


def p_statement_expr(p):
    "statement : expression"
    p[0] = p[1]


def p_statement_assign(p):
    "statement : ID EQUALS expression"
    p[0] = ("assign", p[1], p[3])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_empty(p):
    "empty :"
    p[0] = None


def p_statements_multiple(p):
    "statements : statements statement"
    p[0] = p[1] + [p[2]]


def p_statements_single(p):
    "statements : statement"
    p[0] = [p[1]]


def p_expression_id(p):
    "expression : ID"
    p[0] = ("var", p[1])


def eval_ast_in_env(ast, local_env):
    """
    Evaluates an abstract syntax tree (AST) in the given local environment.

    This function is useful for evaluating ASTs in the context of a function call,
    where local variables need to be taken into account.

    :param ast: The root node of the AST to be evaluated.
    :param local_env: A dictionary representing a local variable environment.
    :return: The result of the evaluation of the AST.
    """
    old_env = env.copy()
    env.update(local_env)
    try:
        return eval_ast(ast, env)
    except ReturnValue as r:
        return r.value
    finally:
        env.clear()
        env.update(old_env)


class ReturnValue(Exception):
    """
    Exception class used to return a value from a function.
    """

    def __init__(self, value):
        """
        Initializes a ReturnValue instance with the given value.

        :param value: The value to be stored in the ReturnValue instance.
        """
        self.value = value


def eval_ast(node, local_env=None):
    """
    Evaluates an abstract syntax tree (AST) and returns its result.

    Supports arithmetic operations, trigonometric functions, power expressions,
    variable assignments, conditionals, loops, and function calls.

    :param node: The root node of the AST to be evaluated.
    :param local_env: Optional dictionary representing a local variable environment.
    :return: The result of the evaluation of the AST.
    """
    env_to_use = local_env if local_env is not None else env

    if isinstance(node, (int, float)):
        return node

    if isinstance(node, list):
        result = None
        for stmt in node:
            result = eval_ast(stmt, env_to_use)
        return result

    if isinstance(node, tuple):
        op = node[0]

        operations = {
            "+": lambda: eval_ast(node[1], env_to_use) + eval_ast(node[2], env_to_use),
            "-": lambda: eval_ast(node[1], env_to_use) - eval_ast(node[2], env_to_use),
            "*": lambda: eval_ast(node[1], env_to_use) * eval_ast(node[2], env_to_use),
            "/": lambda: eval_ast(node[1], env_to_use) / eval_ast(node[2], env_to_use),
            "^": lambda: eval_ast(node[1], env_to_use) ** eval_ast(node[2], env_to_use),
            "<": lambda: eval_ast(node[1]) < eval_ast(node[2]),
            ">": lambda: eval_ast(node[1]) > eval_ast(node[2]),
            "==": lambda: eval_ast(node[1]) == eval_ast(node[2]),
            "!=": lambda: eval_ast(node[1]) != eval_ast(node[2]),
            "<=": lambda: eval_ast(node[1]) <= eval_ast(node[2]),
            ">=": lambda: eval_ast(node[1]) >= eval_ast(node[2]),
            "neg": lambda: -eval_ast(node[1], env_to_use),
            "assign": lambda: env_to_use.update(
                {node[1]: eval_ast(node[2], env_to_use)}
            )
            or env_to_use[node[1]],
            "var": lambda: eval_variable(node[1]),
            "call": lambda: eval_function_call(node[1], node[2], env_to_use),
            "if": lambda: eval_if(node[1], node[2]),
            "if-else": lambda: (
                eval_ast(node[2]) if eval_ast(node[1]) else eval_ast(node[3])
            ),
            "while": lambda: eval_while(node[1], node[2]),
            "block": lambda: eval_block(node[1]),
            "return": lambda: (
                _ := eval_ast(node[1], env_to_use),
                (_ for _ in ()).throw(ReturnValue(_[1])),
            ),
            "def": lambda: functions.update({node[1]: (node[2], node[3])}),
            "print": lambda: print(eval_ast(node[1])),
            "set": lambda: env.update({node[1]: eval_ast(node[2])}),
        }

        if op in operations:
            return operations[op]()

        print(f"Error: unknown operation '{op}'")
        return 0
    return 0


math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "sqrt": math.sqrt,
}


def eval_function_call(name, arg_nodes, env_to_use):
    """
    Evaluates a function call by looking up the function in the global environment.

    If the function is found, it evaluates each argument and calls the function with the
    evaluated arguments. If the function is a built-in function, it calls the corresponding
    function from the math module.

    If the function is not found, it prints an error message and returns 0.

    :param name: The name of the function to be called.
    :param arg_nodes: A list of nodes representing the arguments to the function.
    :param env_to_use: The environment to be used for evaluation.
    :return: The result of the function call, or 0 if an error occurred.
    """
    if name in functions:
        params, body = functions[name]
        if len(params) != len(arg_nodes):
            print(
                f"Error: function '{name}' expected {len(params)}"
                f"arguments, received {len(arg_nodes)}."
            )
            return 0
        local_env = env.copy()
        for param, arg_node in zip(params, arg_nodes):
            local_env[param] = eval_ast(arg_node, env_to_use)
        try:
            return eval_ast(body, local_env)
        except ReturnValue as r:
            return r.value
    elif name in math_functions:
        arg = eval_ast(arg_nodes[0], env_to_use)
        return math_functions[name](arg)
    else:
        print(f"Error: function '{name}' not found.")
        return 0


def eval_variable(name):
    """
    Evaluates a variable by looking it up in the global environment.

    If the variable does not exist in the global environment, it prints an error
    message and returns 0.

    :param name: The name of the variable to be evaluated.
    :return: The value of the variable, or 0 if it does not exist.
    """
    if name in env:
        return env[name]
    print(f"Error: variable '{name}' not found.")
    return 0


def eval_if(condition, block):
    """Evaluates the 'if' expression."""
    if eval_ast(condition):
        return eval_block(block)
    return None


def eval_while(condition, block):
    """Evaluates the 'while' loop."""
    while eval_ast(condition):
        eval_block(block)
    return env.get("x", 0)


def eval_block(statements):
    """Evaluates a block of statements."""
    result = None
    for stmt in statements:
        result = eval_ast(stmt)
    return result


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression POWER expression"""
    p[0] = (p[2], p[1], p[3])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = ("neg", p[2])


def p_expression_func(p):
    """expression : ID LPAREN expression RPAREN"""
    p[0] = ("call", p[1], p[3])


def p_statement_if(p):
    "statement : IF LPAREN expression RPAREN block"
    p[0] = ("if", p[3], p[5])


def p_statement_if_else(p):
    "statement : IF LPAREN expression RPAREN block ELSE block"
    p[0] = ("if-else", p[3], p[5], p[7])


def p_statement_while(p):
    "statement : WHILE LPAREN expression RPAREN block"
    p[0] = ("while", p[3], p[5])


def p_statement_function(p):
    "statement : DEF ID LPAREN opt_params RPAREN block"
    p[0] = ("def", p[2], p[4], p[6])


def p_statement_print(p):
    """statement : PRINT expression"""
    print(eval_ast(p[2]))


def p_statement_set(p):
    """statement : SET ID EQUALS expression"""
    env[p[2]] = eval_ast(p[4])


def p_opt_params(p):
    """opt_params : ID
    | ID COMMA opt_params
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_expression_comparison(p):
    """
    expression : expression LT expression
               | expression GT expression
    """
    p[0] = (p[2], p[1], p[3])


def p_statement_return(p):
    "statement : RETURN expression"
    p[0] = ("return", p[2])


def p_block(p):
    "block : LBRACE statements RBRACE"
    p[0] = ("block", p[2])


def p_error(p):
    """
    Handles errors in the parser.

    This function is called when a syntax error is found during parsing. It prints an
    error message indicating the error and a suggestion to fix it.
    :param p: The token containing the error.
    """
    if p:
        if p.type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "POWER"]:
            print(
                f"Error: operator '{p.type}' without operand. Suggestion: Add an operand before it."
            )
        elif p.type == "LPAREN":
            print(
                "Error: opening parenthesis without a closing one. Suggestion: Add a ')' at the end."
            )
        elif p.type == "RPAREN":
            print(
                "Error: closing parenthesis without an opening one. Suggestion: Add a '(' at the end."
            )
        else:
            print(f"Syntax error at token '{p.value}'.")
    else:
        print("Syntax error: incomplete input. Suggestion: Add a ')' at the end.")


def print_ast(node):
    """
    Converts an abstract syntax tree (AST) node into a human-readable string representation.

    This function recursively traverses the AST and constructs a string that represents the
    structure of the tree. Tuples are interpreted as nodes with a type and children, while
    other types are converted to strings directly.

    :param node: The root node of the AST or a sub-node.
    :return: A string representation of the AST node.
    """
    if isinstance(node, tuple):
        return f"({node[0]} {' '.join(print_ast(child) for child in node[1:])})"

    return str(node)


parser = yacc.yacc()
