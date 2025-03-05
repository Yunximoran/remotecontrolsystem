import platform
def get_cpu_arch_and_instruction_sets():
    cpu_arch = platform.machine()
    instruction_sets = platform.architecture()[1]
    return cpu_arch, instruction_sets
cpu_arch, instruction_sets = get_cpu_arch_and_instruction_sets()
print(f'CPU Architecture: {cpu_arch}')
print(f'Instruction Sets: {instruction_sets}')