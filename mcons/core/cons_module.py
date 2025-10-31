
from sys import argv
from os import path, makedirs

from ..rules.rule import Rule, TargetRule, SourceRule

def get_build_dir(src_dir, root_src_dir):
  if root_src_dir != path.commonpath([root_src_dir, src_dir]):
    print(f"error: {src_dir} is not in {root_src_dir}")
    exit(1)
  else:
    rel = path.relpath(src_dir, root_src_dir)
    return path.abspath(rel)

class ConsModule:
  def __init__(self, pyfile):
    root_src_dir = path.abspath(path.dirname(argv[0]))
    self.src_dir = path.abspath(path.dirname(pyfile))
    self.build_dir = get_build_dir(self.src_dir, root_src_dir)
    makedirs(self.build_dir, exist_ok=True)

  def relative(self, rel):
    p = path.join(self.src_dir, rel, "file")
    return ConsModule(p)

  def src(self, file) -> SourceRule:
    filepath = path.join(self.src_dir, file)
    return SourceRule(filepath)

  def extern_file(self, file) -> SourceRule:
    return SourceRule(file)

  def target(self, file, deps, check_func, build_func) -> TargetRule:
    filepath = path.join(self.build_dir, file)
    build_dir = path.dirname(filepath)
    makedirs(build_dir, exist_ok=True)
    return TargetRule(filepath, deps, check_func, build_func)
