
import threading
from os import path, remove

def memo(func):
  has_eval = False
  value = None
  lock = threading.Lock()
  def f():
    nonlocal has_eval, value
    with lock:
      if not has_eval:
        value = func()
        has_eval = True
      return value
  return f

def remove_file(name):
  try:
    remove(name)
  except:
    None

def replace_ext(filename, new_extension):
  name, ext = path.splitext(filename)
  return name + new_extension
