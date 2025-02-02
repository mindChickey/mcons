
from .env import batch
from .core import need_update
from .command import format_command
from .utils import replace_ext
from .object_rule import cons_object

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
    func(cm, deps)
  return target
