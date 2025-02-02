
import subprocess
import tempfile
from os import path

from .core import check_mark, compare_depends_mtime, need_update
from .command import run_command
from .env import env

def parse_depfile(depfile):
  depfile.seek(0)
  content = depfile.read()
  r = content.split()
  return list(filter(lambda x: x != '\\', r[1:]))

def update_depend(cm, target, line):
  try:
    with tempfile.NamedTemporaryFile(mode='w+') as depfile:
      line1 = line + f" -MM -MF {depfile.name}"
      subprocess.run(line1.split(), cwd=cm.build_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      deps = parse_depfile(depfile)
      env.header_depend.update(target, deps)
      return deps
  except:
    exit(1)

def get_depends(cm, target, target_exist, target_mtime, line):
  if target_exist:
    deps = env.header_depend.get(target, target_mtime)
    if deps: return deps
  return update_depend(cm, target, line)

def object_need_update(cm, target: str, line):
  target_exist = path.exists(target)
  target_mtime = path.getmtime(target) if target_exist else 0

  if check_mark(target, target_exist, target_mtime, line):
    return True
  else:
    deps = get_depends(cm, target, target_exist, target_mtime, line)
    return compare_depends_mtime(target_mtime, deps)

def cons_object(cm, src, obj, compile_templ):
  src1 = cm.src(src)
  target = cm.target(obj)
  line = compile_templ.format(src1, target, **env.config)
  env.compile_commands.push(cm.build_dir, src1, line)

  if object_need_update(cm, target, line):
    update_depend(cm, target, line)
    run_command(cm, line)
  return target
