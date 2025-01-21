
from os import path
import subprocess
import tempfile
from core import check_depend, memo, need_update, cc, parse_depfile

def run_command_output(cwd, line, outfile):
  result = subprocess.run(line.split(), cwd=cwd, stdout=outfile)
  if result.returncode != 0:
    raise f"error status code: {result.returncode}"

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

def cons_object(cm, src, obj, compile_templ):
  def f():
    src1 = cm.src(src)
    target = cm.target(obj)
    if check_depend(cm, target):
      line = compile_templ.format(src1, target)
      run_command(cm.build_dir, line)
      with tempfile.NamedTemporaryFile(mode='w+') as mf:
        line1 = line + f" -MM -MF {mf.name}"
        run_command_output(cm.build_dir, line1, None)
        cc.depend_map[target] = parse_depfile(mf)
    return target
  return memo(f)

def pack_ar(cm, name, sources, compile_templ):
  def f():
    tasks = [cons_object(cm, src, replace_extension(".o")(src), compile_templ) for src in sources]
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
