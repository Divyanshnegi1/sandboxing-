# sandbox_backend.py

from sandbox_security import create_secure_sandbox
from sandbox_exec import exec_code
from sandbox_list_remove import list_sandboxes, remove_sandbox

def create_sandbox(name, memory, cpu):
    try:
        create_secure_sandbox(name, memory, cpu)
        return f"Sandbox '{name}' created successfully.\n"
    except Exception as e:
        return f"Error creating sandbox '{name}': {str(e)}\n"

def execute_code(name, file_path):
    try:
        output = exec_code(name, file_path)
        return output
    except Exception as e:
        return f"Execution failed: {str(e)}\n"

def list_all_sandboxes():
    try:
        containers = list_sandboxes()
        if not containers:
            return "No sandboxes found.\n"
        else:
            result = "Sandboxes:\n"
            for name, short_id, status in containers:
                result += f"- {name} (ID: {short_id}, Status: {status})\n"
            return result
    except Exception as e:
        return f"Error listing sandboxes: {str(e)}\n"

def delete_sandbox(name):
    try:
        remove_sandbox(name)
        return f"Sandbox '{name}' removed successfully.\n"
    except Exception as e:
        return f"Error removing sandbox '{name}': {str(e)}\n"

