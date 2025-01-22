
import tempfile

from .core import need_update
from .thread_pool import batch
from .header_depend import get_header_depend, update_header_depend

from .command import run_command, run_command_output, format_command
from .utils import replace_ext

def check_depend(obj):
  deps = get_header_depend(obj)
  if deps:
    return need_update(obj, deps)
  else:
    return True

def cons_object(cm, src, obj, compile_templ):
  src1 = cm.src(src)
  target = cm.target(obj)
  if check_depend(target):
    line = compile_templ.format(src1, target)
    run_command(cm, line)
    with tempfile.NamedTemporaryFile(mode='w+') as mf:
      line1 = line + f" -MM -MF {mf.name}"
      run_command_output(cm.build_dir, line1, None)
      update_header_depend(target, mf)
  return target

def cons_object_list(cm, sources, ext, compile_templ):
  def f(src):
    return lambda: cons_object(cm, src, replace_ext(src, ext), compile_templ)
  tasks = [f(src) for src in sources]
  return batch(tasks)

def pack_ar(cm, name, sources, compile_templ):
  objects = cons_object_list(cm, sources, ".o", compile_templ)
  cmd = format_command(f"ar rcs {name} {' '.join(objects)}")
  return task(cm, name, objects, cmd)

def task(cm, name, deps, func):
  target = cm.target(name)
  if need_update(target, deps):
    func(cm.build_dir, deps)
  return target
