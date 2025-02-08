
from typing import Iterable

from .rule import TargetRule
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
  target = cm.target(name, deps, None, None)
  deps1 = ' '.join(map(str, deps))
  cmd = templ.format(deps1, target, **env.config)

  def check_func():
    valid = not need_update(target, deps, cmd)
    target.valid = valid
    return valid

  def build_func():
    run_command(cm, cmd)
    target.update()
  
  target.check_func = check_func
  target.build_func = build_func
  return target

def comb_task(deps: Iterable[Rule]):
  return TargetRule("", deps, lambda: True, lambda: None)
