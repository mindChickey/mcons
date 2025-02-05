
import subprocess
from .cons_module import ConsModule

def run_command(cm: ConsModule, line, check=True):
  cwd = cm.build_dir
  try:
    subprocess.run(line.split(), cwd=cwd, check=check)
  except:
    exit(1)
