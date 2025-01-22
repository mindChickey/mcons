
import threading
from os import path, remove

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

def remove_file(name):
  try:
    remove(name)
  except:
    None

def replace_extension(new_extension):
  def f(filename):
    name, ext = path.splitext(filename)
    return name + new_extension
  return f
