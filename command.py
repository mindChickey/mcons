
import subprocess

def run_command_output(cwd, line, outfile):
  result = subprocess.run(line.split(), cwd=cwd, stdout=outfile)
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

def run_command(cwd, line):
  print(cwd, ": ", line)
  result = subprocess.run(line.split(), cwd=cwd, capture_output=True)
  if result.stderr:
    print(result.stderr.decode('utf-8'))
  if result.stdout:
    print(result.stdout.decode('utf-8'))
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

def format_command(templ):
  def f(cwd, deps): 
    return run_command(cwd, templ.format(*deps))
  return f

