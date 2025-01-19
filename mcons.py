
from os import path, stat, makedirs
import subprocess
from typing import List, Union
import dask
from dask import delayed

build_dir = ""
root_dir = ""

def join_string_list(strlist):
  result = []
  for item in strlist:
    if isinstance(item, str):
      result.extend(item.split())
    elif isinstance(item, List):
      result.extend(join_string_list(item))
    else:
      raise "type error"
  return result

def run_command(cwd, *args: Union[str, List[str]]):
  line = join_string_list(args)
  print(cwd, ": ", ' '.join(line))
  result = subprocess.run(line, cwd=cwd, capture_output=True)
  if result.stderr:
    print(result.stderr.decode('utf-8'))
  if result.stdout:
    print(result.stdout.decode('utf-8'))
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

def need_process(target: str, deps: List[str]):
  if not path.exists(target): return True

  target_stat = stat(target)
  for dep in deps:
    if len(dep) == 0: continue
    if not path.exists(dep):
      raise f"error: file not found: {dep}"
    dep_stat = stat(dep)
    if target_stat.st_mtime < dep_stat.st_mtime:
      return True
  return False

def to_delayed(pydir, x): 
  if isinstance(x, str):
    if path.isabs(x):
      return delayed(x) 
    else:
      return delayed(path.join(pydir, x))
  else:
    return x

def get_map_dir(pydir):
  if root_dir != path.commonpath([root_dir, pydir]):
    raise f"error: {pydir} is not in {root_dir}"
  else:
    rel = path.relpath(pydir, root_dir)
    dir = path.join(build_dir, rel)
    makedirs(dir, exist_ok=True)
    return dir

@delayed
def task(pyfile, target, dependencies, func):
  pydir = path.dirname(path.abspath(pyfile))
  dependencies1 = [to_delayed(pydir, x) for x in dependencies]
  deps = dask.compute(dependencies1)[0]
  map_dir = get_map_dir(pydir)

  target1 = path.join(map_dir, target)
  if need_process(target1, deps):
    func(map_dir, deps)
  return target1

def run(root_pyfile, t):
  global build_dir
  global root_dir
  build_dir = path.abspath(path.curdir)
  root_dir = path.dirname(path.abspath(root_pyfile))
  return dask.compute(t)[0]