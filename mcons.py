
import os
import subprocess
from typing import List, Union
import dask
from dask import delayed

def join_command(args: List[Union[str, List[str]]]) -> List[str]:
  result = []
  for item in args:
    if isinstance(item, str):
      result.extend(item.split())
    elif isinstance(item, List):
      for s in item:
        if isinstance(s, str):
          result.extend(s.split()) 
        else:
          raise "type error"
    else:
      raise "type error"
  return result

def run_command(*args: Union[str, List[str]]):
  line = join_command(args)
  print(' '.join(line))
  result = subprocess.run(line, cwd = ".", capture_output=True)
  if result.stderr:
    print(result.stderr.decode('utf-8'))
  if result.stdout:
    print(result.stdout.decode('utf-8'))
  if result.returncode != 0:
    raise f"error status code: 1"

def need_process(target: str, deps: List[str]):
  if not os.path.exists(target): return True

  target_stat = os.stat(target)
  for dep in deps:
    if len(dep) == 0: continue
    if not os.path.exists(dep):
      raise f"error: file not found: {dep}"
    dep_stat = os.stat(dep)
    if target_stat.st_mtime < dep_stat.st_mtime:
      return True
  return False

def to_delayed(x):
  if isinstance(x, str):
    return delayed(x)
  else:
    return x

@delayed
def task(target, dependencies, func):
  dependencies1 = map(to_delayed, dependencies)
  deps = dask.compute(dependencies1)[0]
  if need_process(target, deps):
    func(deps)
  return target

def run(t):
  return dask.compute(t)[0]