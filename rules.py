
import tempfile

from .core import need_update
from .thread_pool import batch
from .header_depend import get_header_depend, update_header_depend

from .command import run_command, run_command_output
from .utils import replace_extension, memo
from .header_depend import get_header_depend, update_header_depend

def check_depend(obj):
  deps = get_header_depend(obj)
  if deps:
    return need_update(obj, deps)
  else:
    return True

def cons_object(cm, src, obj, compile_templ):
  def f():
    src1 = cm.src(src)
    target = cm.target(obj)
    if check_depend(target):
      line = compile_templ.format(src1, target)
      run_command(cm.build_dir, line)
      with tempfile.NamedTemporaryFile(mode='w+') as mf:
        line1 = line + f" -MM -MF {mf.name}"
        run_command_output(cm.build_dir, line1, None)
        update_header_depend(mf)

    return target
  return memo(f)

def pack_ar(cm, name, sources, compile_templ):
  def f():
    tasks = [cons_object(cm, src, replace_extension(".o")(src), compile_templ) for src in sources]
    objects = batch(tasks)
    target = cm.target(name)
    if need_update(target, objects):
      run_command(cm.build_dir, f"ar r {target} {' '.join(objects)}")
    return target
  return memo(f)

def task(cm, name, depends, func):
  def f():
    depends1 = [cm.src(x) if isinstance(x, str) else x for x in depends]
    deps = batch(depends1)
    target = cm.target(name)
    if need_update(target, deps):
      func(cm.build_dir, deps)
    return target
  return memo(f)
