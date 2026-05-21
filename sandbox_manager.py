import sys
from sandbox_security import create_secure_sandbox
from sandbox_exec import exec_code
from sandbox_list_remove import list_sandboxes, remove_sandbox

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 sandbox_manager.py create <name> <memory_limit> <cpu_shares>")
        print("  python3 sandbox_manager.py list")
        print("  python3 sandbox_manager.py remove <name>")
        print("  python3 sandbox_manager.py exec <name> <code_file>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) != 5:
            print("Usage: python3 sandbox_manager.py create <name> <memory_limit> <cpu_shares>")
            sys.exit(1)
        _, _, name, memory_limit, cpu_shares = sys.argv
        create_secure_sandbox(name, memory_limit, cpu_shares)

    elif command == "list":
        list_sandboxes()

    elif command == "remove":
        if len(sys.argv) != 3:
            print("Usage: python3 sandbox_manager.py remove <name>")
            sys.exit(1)
        _, _, name = sys.argv
        remove_sandbox(name)

    elif command == "exec":
        if len(sys.argv) != 4:
            print("Usage: python3 sandbox_manager.py exec <name> <code_file>")
            sys.exit(1)
        _, _, name, code_file = sys.argv
        output = exec_code(name, code_file)
        print(output)

    else:
        print(f"Unsupported command '{command}'")

