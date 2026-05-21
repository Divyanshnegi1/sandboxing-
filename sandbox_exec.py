import docker
import os
import io
import tarfile

client = docker.from_env()

def exec_code(name, file_path):
    output_log = ""

    if not os.path.isfile(file_path):
        return f"File '{file_path}' not found.\n"

    try:
        container = client.containers.get(name)
    except docker.errors.NotFound:
        return f"No sandbox found with name '{name}'.\n"

    if container.status != 'running':
        try:
            container.start()
            output_log += f"Container '{name}' was not running and has been started.\n"
        except docker.errors.APIError as e:
            return f"Failed to start container '{name}': {e.explanation}\n"

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        file_like_object = io.BytesIO()
        with tarfile.open(fileobj=file_like_object, mode='w') as tar:
            tarinfo = tarfile.TarInfo(name=os.path.basename(file_path))
            tarinfo.size = len(data)
            tar.addfile(tarinfo, io.BytesIO(data))
        file_like_object.seek(0)

        container.put_archive(path='/sandbox_data', data=file_like_object.read())
        output_log += f"File '{file_path}' copied to sandbox '{name}'.\n"
    except Exception as e:
        return f"Error copying file: {e}\n"

    try:
        exec_log = container.exec_run(f"python3 /sandbox_data/{os.path.basename(file_path)}", stdout=True, stderr=True)
        output = exec_log.output.decode()
        if exec_log.exit_code == 0:
            output_log += "Execution Output:\n"
            output_log += output
        else:
            output_log += "Code execution failed inside container.\n"
            output_log += "Execution Output:\n"
            output_log += output
    except Exception as e:
        return f"Error during code execution: {e}\n"

    return output_log

