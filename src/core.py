
import sys
from os import path, remove
from watchrun import watch_dir_cmds

from .record_dict import RecordDict

mark_dict = RecordDict("mark_dict.yaml")

def compare_depends_mtime(target_mtime, deps):
  for dep in deps:
    if not path.exists(dep):
      return True
    elif target_mtime < path.getmtime(dep):
      return True
  return False

def check_mark(target: str, target_exist, target_mtime, mark):
  if target_exist:
    mark0 = mark_dict.get(target, target_mtime)
    if mark0 == mark: return False

  mark_dict.update(target, mark)
  return True

def need_update(target: str, deps, mark=None):
  target_exist = path.exists(target)
  target_mtime = path.getmtime(target) if target_exist else 0

  if check_mark(target, target_exist, target_mtime, mark):
    return True
  else:
    return compare_depends_mtime(target_mtime, deps)

def remove_file(name):
  try:
    remove(name)
  except:
    None

def clean_all():
  for name in mark_dict.dict1.keys():
    remove_file(name)

def watch(pyfile, cmds):
  build_cmd = f"{sys.executable} {pyfile}"
  src_dir = path.dirname(pyfile)
  build_dir = path.curdir
  watch_dir_cmds(src_dir, 1, [build_cmd] + cmds, [build_dir])
