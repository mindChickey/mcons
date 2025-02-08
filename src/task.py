
from typing import Iterable
from .cons_module import ConsModule, Rule
from .env import batch, batch_map, env
from .check_depend import need_update
from .command import run_command
from .utils import replace_ext
from .object_rule import object_rule

def cons_object_list(cm: ConsModule, sources: Iterable[str], ext: str, compile_templ: str):
  def f(src):
    return object_rule(cm, src, replace_ext(src, ext), compile_templ)
  return batch_map(f, sources)

def pack_ar(cm: ConsModule, name: str, sources: Iterable[str], compile_templ: str):
  objects = cons_object_list(cm, sources, ".o", compile_templ)
  cmd = "ar rcs {1} {0}"
  return task(cm, name, objects, cmd)

def task(cm: ConsModule, name: str, deps: Iterable[Rule], templ: str):
  target = cm.target(name, deps, None)
  def build_func():
    deps1 = ' '.join(map(str, deps))
    cmd = templ.format(deps1, target, **env.config)
    if need_update(target, deps, cmd):
      print(f"\033[32;1m{target}\033[0m") 
      run_command(cm, cmd)
      target.update()
  
  target.build_func = build_func
  return target