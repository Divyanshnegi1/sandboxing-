import docker

client = docker.from_env()

def list_sandboxes():
    containers = client.containers.list(all=True)
    if not containers:
        print("No sandboxes found.")
    else:
        print("Sandboxes:")
        for c in containers:
            print(f"- {c.name} (ID: {c.short_id}, Status: {c.status})")

def remove_sandbox(name):
    try:
        container = client.containers.get(name)
        if container.status == 'running':
            print(f"Stopping sandbox '{name}'...")
            container.stop()
        print(f"Removing sandbox '{name}'...")
        container.remove()
        print(f"Sandbox '{name}' removed successfully.")
    except docker.errors.NotFound:
        print(f"No sandbox found with name '{name}'.")
    except docker.errors.APIError as e:
        print(f"Error removing sandbox: {e.explanation}")

