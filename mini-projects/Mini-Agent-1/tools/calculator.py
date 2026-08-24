import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def calculator(expression: str) -> float:
    """
    Safely evaluate a basic mathematical expression.
    Supports +, -, *, /, %, and **.
    """

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)

            if isinstance(node.op, ast.USub):
                return -operand

            if isinstance(node.op, ast.UAdd):
                return operand

            raise ValueError("Unsupported unary operator.")

        raise ValueError("Invalid mathematical expression.")

    return evaluate(tree.body)