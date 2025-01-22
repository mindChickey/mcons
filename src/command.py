
from os import remove
import subprocess
from .cons_module import ConsModule

def run_command(cm: ConsModule, line, ignore_error=False):
  cwd = cm.build_dir
  print(cwd, ": ", line)
  result = subprocess.run(line.split(), cwd=cwd)
  if result.returncode != 0 and not ignore_error:
    exit(1)

def format_command(templ):
  def f(cm, deps): 
    return run_command(cm, templ.format(*deps))
  return f

def remove_file(name):
  try:
    remove(name)
  except:
    None

def clean_files(cm: ConsModule, files):
  for file in files:
    remove_file(cm.target(file))
