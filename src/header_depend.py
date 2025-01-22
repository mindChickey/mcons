
import yaml
import atexit
import threading
from os import fstat

def parse_depfile(depfile):
  depfile.seek(0)
  content = depfile.read()
  r = content.split()
  return list(filter(lambda x: x != '\\', r[1:]))

def read_yaml(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      mtime = fstat(f.fileno()).st_mtime
      return (mtime, yaml.safe_load(f))
  except:
    return (0, {})

def save_yaml(filename, depend_map):
  def f():
    with open(filename, 'w', encoding='utf-8') as f:
      yaml.dump(depend_map, f)
  return f

class HeaderDepend:
  def __init__(self, filename):
    self.lock = threading.Lock()
    self.mtime, self.depend_map = read_yaml(filename)
    atexit.register(save_yaml(filename, self.depend_map))

  def get(self, obj):
    with self.lock:
      return self.depend_map.get(obj)
  
  def update(self, target, deps):
    with self.lock:
      self.depend_map[target] = deps

header_depend = HeaderDepend("header_depend.yaml")
