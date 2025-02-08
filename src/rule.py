
from os import path
from typing import List

class Rule:
  def __str__(self):
    return self.filepath

  def update(self):
    try:
      mtime = path.getmtime(self.filepath)
      self.mtime = mtime
      self.valid = True
    except:
      self.mtime = 0
      self.valid = False

class SourceRule(Rule):
  def __init__(self, filepath: str):
    self.filepath = filepath 
    self.update()

class TargetRule(Rule):
  def __init__(self, filepath: str, deps: List[Rule], check_func, build_func):
    self.filepath = filepath
    self.deps = deps
    self.check_func = check_func
    self.build_func = build_func
    self.update()

  def __repr__(self):
      return f"{self.filepath} {self.deps}"
