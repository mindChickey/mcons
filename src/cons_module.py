
from sys import argv
from os import path, makedirs
import threading

def memo_dict(dict, f, key):
  r = dict.get(key)
  if r == None:
    r1 = f(key)
    dict[key] = r1
    return r1
  else:
    return r

def get_build_dir(src_dir, root_src_dir):
  if root_src_dir != path.commonpath([root_src_dir, src_dir]):
    print(f"error: {src_dir} is not in {root_src_dir}")
    exit(1)
  else:
    rel = path.relpath(src_dir, root_src_dir)
    return path.abspath(rel)

class ConsNode:
  def __init__(self, filepath):
    self.filepath = filepath
    self.update()

  def __str__(self):
    return self.filepath

  def update(self):
    try:
      mtime = path.getmtime(self.filepath)
      self.mtime = mtime
      self.exist = True
    except:
      self.mtime = 0
      self.exist = False

class ConsModule:
  def __init__(self, pyfile):
    root_src_dir = path.abspath(path.dirname(argv[0]))
    self.src_dir = path.abspath(path.dirname(pyfile))
    self.build_dir = get_build_dir(self.src_dir, root_src_dir)
    makedirs(self.build_dir, exist_ok=True)
    self.src_dict = {}
    self.target_dict = {}
    self.lock = threading.Lock()

  def src(self, file):
    filepath = path.join(self.src_dir, file)
    with self.lock:
      return memo_dict(self.src_dict, ConsNode, filepath)

  def target(self, file):
    filepath = path.join(self.build_dir, file)
    with self.lock:
      return memo_dict(self.target_dict, ConsNode, filepath)
