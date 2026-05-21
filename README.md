# SecureBox OS

**An AI-Driven Sandboxing Operating System for Secure Isolated Environments**

---

## Project Overview

SecureBox OS is a project designed to create secure, isolated environments using Docker containers. It allows running untrusted or resource-intensive tasks inside sandboxes with strict resource limits and syscall filtering via seccomp profiles.

This helps protect the host system by restricting what sandboxed processes can do, preventing harmful actions or excessive resource consumption.

---

## Features

- Creates isolated Docker containers ("sandboxes") with:
  - Memory limits
  - CPU shares limits
  - Seccomp syscall filtering (using a custom `default.json` profile)
- Programmatic sandbox creation with `sandbox_manager.py`
- Easy to customize resource limits and security profile
- Demonstrated sandbox restrictions via syscall blocking and resource stress tests

---

## Requirements

- Docker installed and running
- Python 3 with `docker` Python package (`pip install docker`)

---

## How to Use

1. Clone or download this project.
2. Make sure `default.json` (seccomp profile) is in the project directory.
3. Run the sandbox manager script to create a sandbox:
    ```bash
    python3 sandbox_manager.py create <name> <memory_limit> <cpu_shares>
    ```
    Example:
    ```bash
    python3 sandbox_manager.py create sandbox1 256m 0.5
    ```
4. Access the sandbox container:
    ```bash
    docker exec -it <name> bash
    ```
5. Run tests or commands inside the sandbox to see restrictions in action.

---

## Example Tests

- Running a memory stress test inside the sandbox:
    ```bash
    docker exec -it sandbox1 stress --vm 1 --vm-bytes 200M --vm-hang 0
    ```
- Trying to create a device node (should fail if blocked by seccomp):
    ```bash
    mknod /tmp/test p
    ```

---

## How it works

- Uses Docker to create isolated containers.
- Enforces resource limits (memory and CPU) using Docker options.
- Applies a seccomp profile (`default.json`) that filters system calls, limiting potentially dangerous operations.
- Can be extended with AI logic to automatically adjust sandbox restrictions based on task characteristics (future work).

---

## Next Steps

- Add monitoring/logging of sandbox activity.
- Integrate AI for dynamic sandbox configuration.
- Expand syscall filtering with custom profiles.

---

## Author

NAVNEET BAHUGUNA
B.Tech Computer Science Engineering  
Graphic Era Hill University  

---

