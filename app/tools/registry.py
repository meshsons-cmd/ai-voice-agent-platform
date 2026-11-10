import ast
import operator
from datetime import datetime, timezone

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
       ast.USub: operator.neg, ast.UAdd: operator.pos}

def _evaluate(expression: str):
    if len(expression) > 200:
        raise ValueError("Expression too long")
    tree = ast.parse(expression, mode="eval")
    def visit(node):
        if isinstance(node, ast.Expression): return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8: raise ValueError("Exponent too large")
            value = OPS[type(node.op)](visit(node.left), right)
            if abs(value) > 10**15: raise ValueError("Result too large")
            return value
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS: return OPS[type(node.op)](visit(node.operand))
        raise ValueError("Unsupported expression")
    return visit(tree)

def calculate(expression: str):
    return {"expression": expression, "result": _evaluate(expression)}

def get_utc_time():
    return {"utc_time": datetime.now(timezone.utc).isoformat()}

TOOL_DEFINITIONS = [
 {"type":"function","function":{"name":"calculate","description":"Safely evaluate arithmetic.",
  "parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"],"additionalProperties":False}}},
 {"type":"function","function":{"name":"get_utc_time","description":"Get current UTC time.",
  "parameters":{"type":"object","properties":{},"additionalProperties":False}}}
]

def execute_tool(name, arguments):
    if name == "calculate": return calculate(str(arguments.get("expression", "")))
    if name == "get_utc_time": return get_utc_time()
    raise ValueError(f"Tool is not allowed: {name}")
