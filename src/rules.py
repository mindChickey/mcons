
from typing import Iterable
from .cons_module import ConsModule, ConsNode
from .env import batch, env, rule
from .check_depend import need_update
from .command import run_command
from .utils import replace_ext
from .object_rule import cons_object

def cons_object_list(cm: ConsModule, sources: Iterable[str], ext: str, compile_templ: str):
  def f(src):
    return lambda: rule(cm, replace_ext(src, ext), cons_object(src, compile_templ))
  tasks = map(f, sources)
  return batch(tasks)

def pack_ar(cm: ConsModule, name, sources: Iterable[str], compile_templ: str):
  objects = cons_object_list(cm, sources, ".o", compile_templ)
  cmd = "ar rcs {1} {0}"
  return rule(cm, name, task(objects, cmd))

def task(deps: Iterable[ConsNode], templ: str):
  def f(cm: ConsModule, target: ConsNode):
    deps1 = ' '.join(map(str, deps))
    cmd = templ.format(deps1, target, **env.config)
    if need_update(target, deps, cmd):
      print(f"\033[32;1m{target}\033[0m") 
      run_command(cm, cmd)
      target.update()
    return target
  return f
