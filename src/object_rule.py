
import subprocess
import tempfile
from os import path

from .core import compare_depends_mtime
from .header_depend import parse_depfile, header_depend
from .compile_commands import compile_commands

from .command import run_command

def update_depend(cm, target, line):
  try:
    with tempfile.NamedTemporaryFile(mode='w+') as depfile:
      line1 = line + f" -MM -MF {depfile.name}"
      subprocess.run(line1.split(), cwd=cm.build_dir, check=True)
      deps = parse_depfile(depfile)
      header_depend.update(target, deps)
      return deps
  except:
    exit(1)

def object_need_update(cm, target, line):
  if not path.exists(target): 
    update_depend(cm, target, line)
    return True

  target_mtime = path.getmtime(target)

  if header_depend.mtime < target_mtime: 
    deps = update_depend(cm, target, line)
    return compare_depends_mtime(target_mtime, deps)

  deps = header_depend.get(target)
  if deps:
    if compare_depends_mtime(target_mtime, deps):
      update_depend(cm, target, line)
      return True
    else:
      return False
  else:
    deps = update_depend(cm, target, line)
    return compare_depends_mtime(target_mtime, deps)

def cons_object(cm, src, obj, compile_templ):
  src1 = cm.src(src)
  target = cm.target(obj)
  line = compile_templ.format(src1, target)
  compile_commands.push(cm.build_dir, src1, line)

  if object_need_update(cm, target, line):
    run_command(cm, line)
  return target
