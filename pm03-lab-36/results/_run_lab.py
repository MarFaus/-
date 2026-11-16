import subprocess, sys, os, textwrap
OUT = '/home/user/work/lab36/out'
def run(fname, cmds, mode='w'):
    """Выполняет команды внутри стенда и пишет в файл '$ команда' + вывод. Возвращает коды выхода."""
    codes = []
    with open(f'{OUT}/{fname}.txt', mode) as f:
        for c in cmds:
            f.write('$ ' + c + '\n')
            r = subprocess.run(['/home/user/work/lab36/sdx', c], capture_output=True, text=True, timeout=900)
            f.write(r.stdout + r.stderr)
            if not (r.stdout + r.stderr).endswith('\n') and (r.stdout + r.stderr): f.write('\n')
            f.write('\n')
            codes.append(r.returncode)
    return codes
if __name__ == '__main__':
    pass
