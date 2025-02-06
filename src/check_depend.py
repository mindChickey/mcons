
from typing import Iterable

from .cons_module import ConsNode
from .env import env

def compare_depends_mtime(target: ConsNode, deps: Iterable[ConsNode]):
  for dep in deps:
    if not dep.exist:
      return True
    elif target.mtime < dep.mtime:
      return True
  return False

def check_mark(target: ConsNode, mark):
  if target.exist:
    mark0 = env.mark_dict.get(target, target.mtime)
    if mark0 == mark: return False

  env.mark_dict.update(target.filepath, mark)
  return True

def need_update(target: ConsNode, deps: Iterable[ConsNode], mark=""):
  if check_mark(target, mark):
    return True
  else:
    return compare_depends_mtime(target, deps)
