"""Modulo interpreter."""

import math

global_env = {}
global_functions = {}
math_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
}


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


def eval_variable(name, env):
    """
    Evaluates a variable and returns its value.

    If the variable is not found in the provided environment, an error message is printed
    and 0 is returned.

    :param name: The name of the variable to be evaluated.
    :param env: The environment in which to evaluate the variable.
    :return: The value of the variable, or 0 if not found.
    """
    if name in env:
        return env[name]
    print(f"Erro: variável '{name}' não encontrada.")
    return 0


def eval_if(condition, block, env):
    """
    Evaluates an if statement and returns the result of the block if the condition is true.

    If the condition is not true, the function returns None.

    :param condition: The condition to be evaluated.
    :param block: The block of statements to be executed if the condition is true.
    :param env: The environment in which to evaluate the if statement.
    :return: The result of the block if the condition is true, or None if not.
    """
    if eval_ast(condition, env):
        return eval_block(block, env)
    return None


def eval_while(condition, block, env):
    """
    Evaluates a while loop and returns the final value of variable x after
    all iterations, or 0 if x is not defined.

    :param condition: An AST node representing the loop condition.
    :param block: An AST node representing the loop body.
    :param env: The environment in which to evaluate the loop.
    :return: The final value of variable x after all iterations, or 0 if x is not defined.
    """
    while eval_ast(condition, env):
        eval_block(block, env)
    return env.get("x", 0)


def eval_block(statements, env):
    """
    Evaluates a block of statements and returns the result of the last statement.

    :param statements: A list of AST nodes representing the statements to be evaluated.
    :param env: The environment in which to evaluate the statements.
    :return: The result of the last statement in the block, or None if the block is empty.
    """
    result = None
    for stmt in statements:
        result = eval_ast(stmt, env)
    return result


def define_function(node, functions):
    """
    Defines a new function with the given name, parameters, and body.

    The function is added to the functions dictionary with its name as the key
    and a tuple of its parameters and body as the value.

    If the function with the given name is already defined, an error message is printed.

    :param node: An AST node representing the function definition.
    :param functions: The dictionary in which to add the function.
    """
    name = node[1]
    params = node[2]
    body = node[3]

    if name in functions:
        print(f"Error: function '{name}' is already defined")
    else:
        functions[name] = (params, body)


def call_user_function(name, arg_nodes, env_to_use):
    """
    Calls a user-defined or mathematical function with specified arguments.

    This function evaluates and calls a user-defined function or a mathematical
    function (like sin, cos, etc.) based on the provided function name and arguments.
    It checks for function definition, argument count, and evaluates the function
    body within a local environment if it is a user-defined function.

    :param name: The name of the function to call.
    :param arg_nodes: A list of AST nodes representing the arguments to the function.
    :param env_to_use: The environment in which to evaluate the function arguments
                       and body.
    :return: The result of the function call, or 0 if an error occurs.
    """

    if name in math_functions:
        return math_functions[name](*arg_nodes)

    if name not in global_functions:
        print(f"Erro: função '{name}' não definida.")
        return 0

    params, body = global_functions[name]

    if len(params) != len(arg_nodes):
        print(
            f"Error: function '{name}' expects {len(params)} "
            "arguments, but {len(arg_nodes)} were provided."
        )
        return 0

    arg_values = [eval_ast(arg, env_to_use) for arg in arg_nodes]

    local_env = env_to_use.copy()
    for param, value in zip(params, arg_values):
        local_env[param] = value

    try:
        return eval_ast(body, local_env)
    except ReturnValue as rv:
        return rv.value


def eval_program(node, env_to_use):
    """
    Evaluates a program by executing its statements in order.

    A program is a sequence of statements. Each statement is evaluated in order
    and the result of the last statement is returned as the result of the program.

    :param node: The AST node representing the program to be evaluated.
    :param local_env: Optional dictionary representing a local variable environment.
    :return: The result of the evaluation of the last statement in the program.
    """
    result = None
    for stmt in node[1]:
        result = eval_ast(stmt, env_to_use)
    return result


def eval_ast(node, local_env=None):
    """
    Evaluates an abstract syntax tree (AST) and returns its result.

    Supports arithmetic operations, trigonometric functions, power expressions,
    variable assignments, conditionals, loops, and function calls.

    :param node: The root node of the AST to be evaluated.
    :param local_env: Optional dictionary representing a local variable environment.
    :return: The result of the evaluation of the AST.
    """
    env_to_use = local_env if local_env is not None else global_env

    if isinstance(node, (int, float)):
        return node

    if isinstance(node, list):
        result = None
        for stmt in node:
            result = eval_ast(stmt, env_to_use)
        return result

    if isinstance(node, tuple):
        op = node[0]

        if op == "def":
            define_function(node, global_functions)
            return None

        operations = {
            "+": lambda: eval_ast(node[1], env_to_use) + eval_ast(node[2], env_to_use),
            "-": lambda: eval_ast(node[1], env_to_use) - eval_ast(node[2], env_to_use),
            "*": lambda: eval_ast(node[1], env_to_use) * eval_ast(node[2], env_to_use),
            "/": lambda: (
                eval_ast(node[1], env_to_use) / eval_ast(node[2], env_to_use)
                if eval_ast(node[2], env_to_use) != 0
                else (print("Error: division by zero") or 0)
            ),
            "^": lambda: eval_ast(node[1], env_to_use) ** eval_ast(node[2], env_to_use),
            "<": lambda: eval_ast(node[1], env_to_use) < eval_ast(node[2], env_to_use),
            ">": lambda: eval_ast(node[1], env_to_use) > eval_ast(node[2], env_to_use),
            "==": lambda: eval_ast(node[1], env_to_use)
            == eval_ast(node[2], env_to_use),
            "!=": lambda: eval_ast(node[1], env_to_use)
            != eval_ast(node[2], env_to_use),
            "<=": lambda: eval_ast(node[1], env_to_use)
            <= eval_ast(node[2], env_to_use),
            ">=": lambda: eval_ast(node[1], env_to_use)
            >= eval_ast(node[2], env_to_use),
            "neg": lambda: -eval_ast(node[1], env_to_use),
            "assign": lambda: (
                env_to_use.update({node[1]: eval_ast(node[2], env_to_use)})
                or env_to_use[node[1]]
            ),
            "var": lambda: eval_variable(node[1], env_to_use),
            "call": lambda: call_user_function(node[1], node[2], env_to_use),
            "if": lambda: eval_if(node[1], node[2], env_to_use),
            "if-else": lambda: (
                eval_ast(node[2], env_to_use)
                if eval_ast(node[1], env_to_use)
                else eval_ast(node[3], env_to_use)
            ),
            "while": lambda: eval_while(node[1], node[2], env_to_use),
            "block": lambda: eval_block(node[1], env_to_use),
            "return": lambda: (_ for _ in ()).throw(
                ReturnValue(eval_ast(node[1], env_to_use))
            ),
            "print": lambda: print(eval_ast(node[1], env_to_use)),
            "program": lambda: eval_program(node, env_to_use),
        }

        if op in operations:
            return operations[op]()

        print(f"Error: unknown operator '{op}'.")
        return 0

    return 0


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
