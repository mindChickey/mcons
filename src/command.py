
from os import remove
import subprocess
from .cons_module import ConsModule

def run_command_output(cwd, line, outfile):
  result = subprocess.run(line.split(), cwd=cwd, stdout=outfile)
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

def run_command(cm: ConsModule, line):
  cwd = cm.build_dir
  print(cwd, ": ", line)
  result = subprocess.run(line.split(), cwd=cwd, capture_output=True)
  if result.stderr:
    print(result.stderr.decode('utf-8'))
  if result.stdout:
    print(result.stdout.decode('utf-8'))
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

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
