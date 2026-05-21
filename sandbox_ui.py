import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import os
import threading

from sandbox_security import create_secure_sandbox
from sandbox_list_remove import list_sandboxes, remove_sandbox
from sandbox_exec import exec_code
from ai_analysis import analyze_code
from resource_monitor import get_container_stats

class SecureBoxUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ShieldBox UI")
        self.selected_file = None

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="ShieldBox ", font=("Helvetica", 16)).pack(pady=10)

        # Create Sandbox
        frame_create = tk.LabelFrame(self.root, text="Create Sandbox")
        frame_create.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_create, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(frame_create)
        self.name_entry.grid(row=0, column=1)

        tk.Label(frame_create, text="Memory :").grid(row=1, column=0)
        self.mem_entry = tk.Entry(frame_create)
        self.mem_entry.grid(row=1, column=1)

        tk.Label(frame_create, text="CPU Shares :").grid(row=2, column=0)
        self.cpu_entry = tk.Entry(frame_create)
        self.cpu_entry.grid(row=2, column=1)

        tk.Button(frame_create, text="Create", command=self.create_sandbox).grid(row=3, columnspan=2, pady=5)

        # Sandbox Management
        frame_manage = tk.LabelFrame(self.root, text="Manage Sandbox")
        frame_manage.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_manage, text="List Sandboxes", command=list_sandboxes).pack(side="left", padx=5)
        tk.Button(frame_manage, text="Remove Sandbox", command=self.remove_sandbox).pack(side="left", padx=5)

        # Code Execution
        frame_exec = tk.LabelFrame(self.root, text="Execute Code")
        frame_exec.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_exec, text="Select File", command=self.select_file).pack(side="left", padx=5)
        self.file_label = tk.Label(frame_exec, text="No file selected")
        self.file_label.pack(side="left")

        tk.Button(frame_exec, text="Run Code", command=self.run_code_thread).pack(side="left", padx=5)

        # Output Box
        frame_output = tk.LabelFrame(self.root, text="Output")
        frame_output.pack(fill="both", expand=True, padx=10, pady=5)

        self.output_text = scrolledtext.ScrolledText(frame_output, wrap="word", height=20)
        self.output_text.pack(fill="both", expand=True)

    def log(self, message):
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)

    def create_sandbox(self):
        name = self.name_entry.get()
        mem = self.mem_entry.get()
        cpu = self.cpu_entry.get()
        if not all([name, mem, cpu]):
            messagebox.showerror("Error", "All fields are required")
            return
        create_secure_sandbox(name, mem, cpu)

    def remove_sandbox(self):
        name = simpledialog.askstring("Remove Sandbox", "Enter sandbox name to remove:")
        if name:
            remove_sandbox(name)

    def select_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.selected_file:
            self.file_label.config(text=os.path.basename(self.selected_file))

    def run_code_thread(self):
        threading.Thread(target=self.run_code).start()

    def run_code(self):
        name = self.name_entry.get()
        if not all([name, self.selected_file]):
            messagebox.showerror("Error", "Sandbox name and code file are required")
            return

        self.output_text.delete(1.0, tk.END)
        output = exec_code(name, self.selected_file)
        self.log(output)

        self.log("\n--- Static Analysis ---")
        self.log(analyze_code(self.selected_file))

        self.log("\n--- Resource Usage ---")
        self.log(get_container_stats(name))

if __name__ == '__main__':
    root = tk.Tk()
    app = SecureBoxUI(root)
    root.mainloop()


