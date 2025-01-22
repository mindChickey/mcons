
from os import path

def need_update(target: str, deps):
  if not path.exists(target): return True
  target_mtime = path.getmtime(target)

  for dep in deps:
    if not path.exists(dep):
      return True
    elif target_mtime < path.getmtime(dep):
      return True
  return False
