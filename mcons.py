
from os import path
import subprocess
from core import memo, need_update, cc

def run_command(cwd, line):
  print(cwd, ": ", line)
  result = subprocess.run(line.split(), cwd=cwd, capture_output=True)
  if result.stderr:
    print(result.stderr.decode('utf-8'))
  if result.stdout:
    print(result.stdout.decode('utf-8'))
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

def format_command(templ):
  def f(cwd, deps): 
    return run_command(cwd, templ.format(*deps))
  return f

def replace_extension(new_extension):
  def f(filename):
    name, ext = path.splitext(filename)
    return name + new_extension
  return f

def cons_object(cm, src, func):
  def f():
    src1 = cm.src(src)
    obj = cm.target(replace_extension(".o")(src))
    if need_update(obj, [src1]):
      func(cm.build_dir, [src1, obj])
    return obj
  return memo(f)

def pack_ar(cm, name, sources, func):
  def f():
    tasks = [cons_object(cm, src, func) for src in sources]
    objects = cc.compute(tasks)
    target = cm.target(name)
    if need_update(target, objects):
      run_command(cm.build_dir, f"ar r {target} {' '.join(objects)}")
    return target
  return memo(f)

def task(cm, name, depends, func):
  def f():
    depends1 = [cm.src(x) if isinstance(x, str) else x for x in depends]
    deps = cc.compute(depends1)
    target = cm.target(name)
    if need_update(target, deps):
      func(cm.build_dir, deps)
    return target
  return memo(f)
