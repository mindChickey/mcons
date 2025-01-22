
from os import path, stat

def need_update(target: str, deps):
  if not path.exists(target): return True

  target_stat = stat(target)
  for dep in deps:
    if not path.exists(dep):
      raise f"error: file not found: {dep}"
    elif target_stat.st_mtime < stat(dep).st_mtime:
      return True
  return False
