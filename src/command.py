
import subprocess
from .cons_module import ConsModule
from .env import env

def run_command(cm: ConsModule, line, check=True):
  cwd = cm.build_dir
  print(cwd, ": ", line)
  try:
    subprocess.run(line.split(), cwd=cwd, check=check)
  except:
    exit(1)

def format_command(templ):
  def f(cm, deps): 
    return run_command(cm, templ.format(*deps, **env.config))
  return f
