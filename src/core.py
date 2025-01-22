
from os import path

def compare_depends_mtime(target_mtime, deps):
  for dep in deps:
    if not path.exists(dep):
      return True
    elif target_mtime < path.getmtime(dep):
      return True
  return False

def need_update(target: str, deps):
  if path.exists(target): 
    target_mtime = path.getmtime(target)
    return compare_depends_mtime(target_mtime, deps)
  else:
    return True