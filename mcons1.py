
import sys
import subprocess
import concurrent.futures
from typing import List, Union
from os import path, stat, makedirs

class ConsContext:
  executor = None
  def __init__(self):
    self.executor = concurrent.futures.ThreadPoolExecutor()

  def __del__(self):
    self.executor.shutdown()

  def compute(self, tasks):
    if(len(tasks) == 0): 
      return []
    else:
      futures = [self.executor.submit(task) for task in tasks[1:]]
      r0 = tasks[0]()
      return [r0] + [future.result() for future in futures]

cc = ConsContext()

def get_build_dir(src_dir, root_src_dir):
  if root_src_dir != path.commonpath([root_src_dir, src_dir]):
    raise f"error: {src_dir} is not in {root_src_dir}"
  else:
    rel = path.relpath(src_dir, root_src_dir)
    return path.abspath(rel)

class ConsModule:
  src_dir = ""
  build_dir = ""
  def __init__(self, pyfile):
    root_src_dir = path.abspath(path.dirname(sys.argv[0]))
    self.src_dir = path.abspath(path.dirname(pyfile))
    self.build_dir = get_build_dir(self.src_dir, root_src_dir)
    makedirs(self.build_dir, exist_ok=True)

  def src(self, file):
    return path.join(self.src_dir, file)

  def target(self, file):
    return path.join(self.build_dir, file)

def need_process(target: str, deps: List[str]):
  if not path.exists(target): return True

  target_stat = stat(target)
  for dep in deps:
    if len(dep) == 0:
      continue
    elif not path.exists(dep):
      raise f"error: file not found: {dep}"
    elif target_stat.st_mtime < stat(dep).st_mtime:
      return True
  return False

####################################

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

def format_command(templ):
  def f(cwd, deps): 
    return run_command(cwd, templ.format(*deps))
  return f

def replace_extension(new_extension):
  def f(filename):
    name, ext = path.splitext(filename)
    return name + new_extension
  return f

def cons_object(cm, src, func):
  def f():
    src1 = cm.src(src)
    obj = cm.target(replace_extension(".o")(src))
    if need_process(obj, [src1]):
      func(cm.build_dir, [src1, obj])
    return obj
  return f

def pack_ar(cm, name, sources, func):
  def f():
    tasks = [cons_object(cm, src, func) for src in sources]
    objects = cc.compute(tasks)
    target = cm.target(name)
    if need_process(target, objects):
      run_command(cm.build_dir, f"ar r {target} {' '.join(objects)}")
    return target
  return f
