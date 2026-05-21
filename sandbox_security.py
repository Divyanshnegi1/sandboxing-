import docker
import os
import time

client = docker.from_env()

def create_secure_sandbox(name, memory_limit, cpu_shares):
    # Add 'm' suffix if not already present for Docker memory limit
    if not memory_limit.lower().endswith(('m', 'g')):
        memory_limit = f"{memory_limit}m"  # assume megabytes if no unit provided

    seccomp_profile_path = os.path.abspath("default.json")

    # Read seccomp profile JSON content as string
    try:
        with open(seccomp_profile_path) as f:
            seccomp_profile_json = f.read()
    except FileNotFoundError:
        print(f"Seccomp profile file not found at {seccomp_profile_path}")
        return

    # Ensure host directory for volume mount exists
    host_sandbox_dir = os.path.abspath("sandbox_data")
    if not os.path.exists(host_sandbox_dir):
        os.makedirs(host_sandbox_dir)

    try:
        container = client.containers.run(
            "python:3.10-slim",
            name=name,
            detach=True,
            tty=True,
            stdin_open=True,
            mem_limit=memory_limit,  # with units like '64m'
            cpu_shares=int(float(cpu_shares) * 1024),
            security_opt=[f"seccomp={seccomp_profile_json}"],
            command="tail -f /dev/null",  # keep container running indefinitely
            volumes={host_sandbox_dir: {'bind': '/sandbox_data', 'mode': 'rw'}},
            cap_drop=["ALL"],
            cap_add=["CHOWN", "SETUID", "SETGID"],
            read_only=True,
            tmpfs={'/tmp': ''},
        )
        print(f"Sandbox '{name}' created successfully.")
        time.sleep(5)  # give container a moment to start
    except docker.errors.APIError as e:
        print(f"Error creating sandbox: {e.explanation}")

