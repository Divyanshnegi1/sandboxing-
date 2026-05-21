import docker
import time

client = docker.from_env()

def get_container_stats(name):
    try:
        container = client.containers.get(name)
        stats = container.stats(stream=False)
        cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
        mem_usage = stats["memory_stats"]["usage"]
        mem_limit = stats["memory_stats"]["limit"]

        usage_mb = round(mem_usage / (1024 * 1024), 2)
        cpu_sec = round(cpu_usage / 1e9, 2)

        return f"📈 Memory Used: {usage_mb} MB | CPU Time: {cpu_sec} sec"

    except Exception as e:
        return f"Error retrieving stats: {e}"

