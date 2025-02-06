
import subprocess
import tempfile
from os import path

from .cons_module import ConsModule, ConsNode
from .check_depend import check_mark, compare_depends_mtime
from .command import run_command
from .env import env

def parse_depfile(depfile):
  depfile.seek(0)
  content = depfile.read()
  r = content.split()
  return list(filter(lambda x: x != '\\', r[1:]))

def update_depend(cm: ConsModule, target: ConsNode, line: str):
  cwd = cm.build_dir
  try:
    with tempfile.NamedTemporaryFile(mode='w+') as depfile:
      line1 = line + f" -MM -MF {depfile.name}"
      subprocess.run(line1.split(), cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      deps = parse_depfile(depfile)
      env.header_depend.update(target.filepath, deps)
      return deps
  except:
    print("update_depend error:", cwd, ":", line)
    exit(1)

def get_depends(cm: ConsModule, target: ConsNode, line: str):
  if target.exist:
    deps = env.header_depend.get(target, target.mtime)
    if deps: return deps
  return update_depend(cm, target, line)

def object_need_update(cm: ConsModule, target: ConsNode, line: str):
  if check_mark(target, line):
    return True
  else:
    deps = get_depends(cm, target, line)
    return compare_depends_mtime(target, deps)

def cons_object(cm: ConsModule, src: str, obj: str, compile_templ: str):
  src1 = cm.src(src)
  target = cm.target(obj)
  line = compile_templ.format(src1, target, **env.config)
  env.compile_commands.push(cm.build_dir, src1.filepath, line)

  if object_need_update(cm, target, line):
    print(f"\033[32m{target}\033[0m")
    update_depend(cm, target, line)
    run_command(cm, line)
  return target
