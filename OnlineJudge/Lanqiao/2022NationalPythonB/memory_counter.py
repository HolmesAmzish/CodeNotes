def solve():
    t = int(input())
    total_bytes = 0
    for _ in range(t):
        line = input().strip()
        if '[' in line:
            parts = line.split()
            data_type = parts[0][:-2]
            var_defs = " ".join(parts[2:]).split(',')
            for var_def in var_defs:
                size_str = var_def.split('[')[1].split(']')[0]
                size = int(size_str)
                if data_type == 'int':
                    total_bytes += size * 4
                elif data_type == 'long':
                    total_bytes += size * 8
        else:
            parts = line.split()
            data_type = parts[0]
            var_defs_str = " ".join(parts[1:]).split(';')[:-1][0]
            var_defs = var_defs_str.split(',')
            for var_def in var_defs:
                if '=' in var_def:
                    var_name, value = var_def.split('=', 1)
                    if data_type == 'int':
                        total_bytes += 4
                    elif data_type == 'long':
                        total_bytes += 8
                    elif data_type == 'String':
                        if value.startswith('"') and value.endswith('"'):
                            total_bytes += len(value) - 2
                        elif value == "''":
                            total_bytes += 0

    gb = total_bytes // (1024 ** 3)
    remaining_bytes = total_bytes % (1024 ** 3)
    mb = remaining_bytes // (1024 ** 2)
    remaining_bytes %= (1024 ** 2)
    kb = remaining_bytes // 1024
    b = remaining_bytes % 1024

    output = []
    if gb > 0:
        output.append(f"{gb}GB")
    if mb > 0:
        output.append(f"{mb}MB")
    if kb > 0:
        output.append(f"{kb}KB")
    if b > 0 or not output:
        output.append(f"{b}B")

    print("".join(output))

if __name__ == "__main__":
    solve()