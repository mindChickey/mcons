
import tempfile
from os import path

from .core import compare_depends_mtime
from .header_depend import parse_depfile, header_depend

from .command import run_command, run_command_output

def update_depend(cm, target, line):
  with tempfile.NamedTemporaryFile(mode='w+') as depfile:
    line1 = line + f" -MM -MF {depfile.name}"
    run_command_output(cm.build_dir, line1, None)
    deps = parse_depfile(depfile)
    header_depend.update(target, deps)
    return deps

def compile_if_need(cm, target_mtime, deps, line):
  if compare_depends_mtime(target_mtime, deps):
    run_command(cm, line)

def cons_object(cm, src, obj, compile_templ):
  src1 = cm.src(src)
  target = cm.target(obj)
  line = compile_templ.format(src1, target)

  if not path.exists(target): 
    update_depend(cm, target, line)
    run_command(cm, line)
    return target

  target_mtime = path.getmtime(target)

  if header_depend.mtime < target_mtime: 
    deps = update_depend(cm, target, line)
    compile_if_need(cm, target_mtime, deps, line)
    return target

  deps = header_depend.get(target)
  if deps:
    compile_if_need(cm, target_mtime, deps, line)
    return target
  else:
    deps = update_depend(cm, target, line)
    compile_if_need(cm, target_mtime, deps, line)
    return target
