def validate_memory_limit(mem):
    # Simple check: memory string ends with 'm' or 'g' and starts with number
    if not (mem.lower().endswith('m') or mem.lower().endswith('g')):
        raise ValueError("Memory limit must end with 'm' or 'g' (e.g. 256m, 1g)")
    try:
        int(mem[:-1])
    except ValueError:
        raise ValueError("Memory limit must be a number followed by 'm' or 'g' (e.g. 256m, 1g)")

def validate_cpu_shares(cpu):
    try:
        val = float(cpu)
        if not (0 < val <= 1):
            raise ValueError("CPU shares must be a decimal between 0 and 1 (e.g. 0.5)")
    except ValueError:
        raise ValueError("CPU shares must be a decimal number (e.g. 0.5)")

