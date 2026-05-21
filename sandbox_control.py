# sandbox_control.py
import docker

client = docker.from_env()

def pause_sandbox(name):
    try:
        container = client.containers.get(name)
        container.pause()
        return f"Sandbox '{name}' paused."
    except Exception as e:
        return f"Error pausing sandbox '{name}': {e}"

def resume_sandbox(name):
    try:
        container = client.containers.get(name)
        container.unpause()
        return f"Sandbox '{name}' resumed."
    except Exception as e:
        return f"Error resuming sandbox '{name}': {e}"

def start_sandbox(name):
    try:
        container = client.containers.get(name)
        if container.status != 'running':
            container.start()
        return f"Sandbox '{name}' started."
    except Exception as e:
        return f"Error starting sandbox '{name}': {e}"

def stop_sandbox(name):
    try:
        container = client.containers.get(name)
        if container.status == 'running':
            container.stop()
        return f"Sandbox '{name}' stopped."
    except Exception as e:
        return f"Error stopping sandbox '{name}': {e}"

def get_sandbox_status(name):
    try:
        container = client.containers.get(name)
        return f"{container.name}: {container.status}"
    except Exception:
        return f"Sandbox '{name}' not found."

