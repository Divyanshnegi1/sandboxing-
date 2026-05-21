import ast

def analyze_code(file_path):
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)

        risky_modules = ['os', 'sys', 'subprocess', 'shutil', 'socket']
        risky_calls = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    if n.name in risky_modules:
                        imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module in risky_modules:
                    imports.append(node.module)
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id in ['eval', 'exec', 'open']:
                    risky_calls.append(node.func.id)
                elif hasattr(node.func, 'attr') and node.func.attr in ['system', 'popen']:
                    risky_calls.append(node.func.attr)

        report = ""
        if imports:
            report += f"Risky imports found: {', '.join(imports)}\n"
        if risky_calls:
            report += f"Risky function calls used: {', '.join(risky_calls)}\n"

        if not report:
            report = "No obvious risky patterns found."

        return report

    except Exception as e:
        return f"Error analyzing code: {e}"

