
import threading

from .record_dict import RecordDict
from .thread_pool import ThreadPool
from .compile_commands import CompileCommands

def memo_dict(dict, f, key):
  r = dict.get(key)
  if r == None:
    r1 = f(key)
    dict[key] = r1
    return r1
  else:
    return r

def empty_rule(cm, name: str, build_func):
  print("env.rule is empty")
  exit(1)

class Env:
  def __init__(self):
    self.config = {}
    self.config_filename = "mcons_config.yaml"
    self.mark_dict_filename = "mark_dict.yaml"
    self.header_depend_filename = "header_depend.yaml"
    self.compile_commands_filename = "compile_commands.json"

    self.lock = threading.Lock()
    self.node_dict = {}
    self.rule = empty_rule

  def init_clean(self, thread_num):
    self.thread_pool = ThreadPool(thread_num)

  def init_build(self, thread_num):
    self.mark_dict = RecordDict(self.mark_dict_filename)
    self.header_depend = RecordDict(self.header_depend_filename)
    self.compile_commands = CompileCommands(self.compile_commands_filename)
    self.thread_pool = ThreadPool(thread_num)

  def get_node(self, f, filepath):
    with self.lock:
      return memo_dict(self.node_dict, f, filepath)

env = Env()

def batch(tasks):
  return env.thread_pool.batch(tasks)

def rule(cm, name:str, build_func):
  return env.rule(cm, name, build_func)
