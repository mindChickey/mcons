
from .env import batch, env
from .check_depend import need_update
from .command import run_command
from .utils import replace_ext
from .object_rule import cons_object

def cons_object_list(cm, sources, ext, compile_templ):
  def f(src):
    return lambda: cons_object(cm, src, replace_ext(src, ext), compile_templ)
  tasks = [f(src) for src in sources]
  return batch(tasks)

def pack_ar(cm, name, sources, compile_templ):
  objects = cons_object_list(cm, sources, ".o", compile_templ)
  cmd = "ar rcs {1} {0}"
  return task(cm, name, objects, cmd)

def task(cm, name, deps, templ):
  target = cm.target(name)
  deps1 = ' '.join(deps)
  cmd = templ.format(deps1, target, **env.config)
  if need_update(target, deps, cmd):
    run_command(cm, cmd)
  return target
