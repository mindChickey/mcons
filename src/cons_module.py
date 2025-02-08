
from sys import argv
from os import path, makedirs

from .rule import Rule, TargetRule, SourceRule

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

  # def src(self, file) -> ConsNode:
  #   filepath = path.join(self.src_dir, file)
  #   f = lambda x: ConsNode(x, [])
  #   return env.get_node(f, filepath)

  # def target(self, file, deps, build_func) -> ConsNode:
  #   filepath = path.join(self.build_dir, file)
  #   f = lambda x: ConsNode(x, deps, build_func)
  #   return env.get_node(f, filepath)

  def src(self, file) -> SourceRule:
    filepath = path.join(self.src_dir, file)
    return SourceRule(filepath)

  def target(self, file, deps, build_func) -> TargetRule:
    filepath = path.join(self.build_dir, file)
    return TargetRule(filepath, deps, build_func)
