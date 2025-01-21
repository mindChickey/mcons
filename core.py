
import atexit
import sys
import yaml
import threading
import concurrent.futures
from os import path, stat, makedirs

def memo(func):
  has_eval = False
  value = None
  lock = threading.Lock()
  def f(*argv):
    nonlocal has_eval, value
    with lock:
      if not has_eval:
        value = func(*argv)
        has_eval = True
      return value
  return f

def read_depend_map():
  try:
    with open("depend_map.yaml", 'r', encoding='utf-8') as f:
      return yaml.safe_load(f)
  except:
    return {}

def save_depend_map(depend_map):
  def f():
    with open('depend_map.yaml', 'w', encoding='utf-8') as f:
      yaml.dump(depend_map, f)
  return f

class ConsContext:
  def __init__(self):
    self.executor = concurrent.futures.ThreadPoolExecutor()
    self.depend_map = read_depend_map()
    atexit.register(save_depend_map(self.depend_map))

  def __del__(self):
    self.executor.shutdown()

  def compute(self, tasks):
    futures = [self.executor.submit(task) for task in tasks]
    results = []
    i = len(tasks)
    while i > 0:
      index = i - 1
      if futures[index].cancel():
        results.append(tasks[index]())
        i = index
      else:
        break

    results0 = [future.result() for future in futures[0:i]]
    results.reverse()
    return results0 + results

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

def need_update(target: str, deps):
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

def check_depend(cm, obj):
  deps = cc.depend_map.get(obj)
  if deps:
    return need_update(obj, [cm.src(dep) for dep in deps])
  else:
    return True

def parse_depfile(mf):
  mf.seek(0)
  content = mf.read()
  r = content.split()
  r1 = list(filter(lambda x: x != '\\', r[1:]))
  return r1
