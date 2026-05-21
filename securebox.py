import os
import sys
import tempfile
import subprocess
import resource
import shutil
import time
import uuid
import signal
from pathlib import Path

class SecureBox:
    def __init__(self, memory_limit_mb=64, cpu_time_limit_sec=2, sandbox_name=None):
        self.memory_limit = memory_limit_mb * 1024 * 1024
        self.cpu_time_limit = cpu_time_limit_sec
        self.sandbox_id = sandbox_name or f"securebox_{uuid.uuid4().hex[:8]}"
        self.temp_dir = tempfile.mkdtemp(prefix=self.sandbox_id + "_")
        self.logs = {
            'stdout': '',
            'stderr': '',
            'status': 'initialized',
            'start_time': None,
            'end_time': None,
        }
        self.forbidden_commands = ['rm', 'shutdown', 'reboot', 'mkfs', 'dd', ':(){', 'fork']

    def log(self, msg):
        print(f"[{self.sandbox_id}] {msg}")

    def is_command_safe(self, command):
        for forbidden in self.forbidden_commands:
            if forbidden in command:
                return False
        return True

    def set_limits(self):
        # Memory
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
        # CPU
        resource.setrlimit(resource.RLIMIT_CPU, (self.cpu_time_limit, self.cpu_time_limit))

    def run(self, command, safe_shell=True):
        self.logs['start_time'] = time.time()

        if safe_shell and not self.is_command_safe(command):
            self.logs['stderr'] = 'Unsafe command blocked.'
            self.logs['status'] = 'blocked'
            self.log('Unsafe command detected and blocked.')
            return

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.cpu_time_limit + 1,
                preexec_fn=self.set_limits
            )
            self.logs['stdout'] = result.stdout
            self.logs['stderr'] = result.stderr
            self.logs['status'] = 'completed'
            self.log('Execution completed.')
        except subprocess.TimeoutExpired:
            self.logs['stderr'] = 'Execution timed out.'
            self.logs['status'] = 'timeout'
            self.log('Execution timed out.')
        except Exception as e:
            self.logs['stderr'] = str(e)
            self.logs['status'] = 'error'
            self.log(f'Execution error: {e}')

        self.logs['end_time'] = time.time()

    def write_file(self, filename, content):
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        self.log(f'File written: {filename}')
        return filepath

    def read_file(self, filename):
        filepath = os.path.join(self.temp_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
        return None

    def list_files(self):
        return os.listdir(self.temp_dir)

    def cleanup(self):
        shutil.rmtree(self.temp_dir)
        self.log('Sandbox cleaned up.')

    def get_logs(self):
        return self.logs

    def print_logs(self):
        print("\n=== Execution Logs ===")
        for k, v in self.logs.items():
            if k in ['start_time', 'end_time'] and v:
                v = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v))
            print(f"{k}: {v}")
        print("======================\n")

# === TESTING / DEMO ===
def example_python_script():
    return '''
print("Welcome to SecureBox!")
for i in range(5):
    print("Running iteration", i)
    
open('unauthorized.txt', 'w').write('This file should not persist.')
'''

def demo():
    box = SecureBox(memory_limit_mb=16, cpu_time_limit_sec=1)
    script = example_python_script()
    script_file = box.write_file("script.py", script)
    box.run(f"python3 {script_file}")
    box.print_logs()
    print("\nFiles in sandbox:", box.list_files())
    print("Output file (unauthorized.txt):")
    print(box.read_file('unauthorized.txt'))
    box.cleanup()

if __name__ == '__main__':
    demo()
