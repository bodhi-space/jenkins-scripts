import subprocess
import sys


def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print(output.strip())
    except subprocess.CalledProcessError as exc:
        print(exc.output.strip())
        sys.exit(1)
