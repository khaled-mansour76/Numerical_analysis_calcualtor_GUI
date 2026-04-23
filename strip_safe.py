import ast
import os

def remove_comments_docstrings(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    # If it's main.py keep shebang
    lines = source.splitlines()
    shebang = ""
    if lines and lines[0].startswith("#!"):
        shebang = lines[0] + "\n"

    try:
        parsed_ast = ast.parse(source)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return

    # Remove docstrings
    for node in ast.walk(parsed_ast):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            continue
        if not len(node.body):
            continue
        if not isinstance(node.body[0], ast.Expr):
            continue
        if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Constant):
            continue
        if getattr(node.body[0].value, 'value', None) is not None and isinstance(node.body[0].value.value, str):
            node.body.pop(0)

    # unparse back to source (removes all comments natively!)
    cleaned = ast.unparse(parsed_ast)
    
    with open(filepath, 'w') as f:
        f.write(shebang + cleaned + "\n")
    print(f"Cleaned {filepath}")

for f in os.listdir('.'):
    if f.endswith('.py') and f not in ('test_all.py', 'test_errors.py', 'strip_safe.py', 'strip_comments.py'):
        remove_comments_docstrings(f)

