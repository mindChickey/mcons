
import sys

from .record_dict import read_yaml, save_yaml, RecordDict
from .thread_pool import ThreadPool
from .compile_commands import CompileCommands

class Env:
  def __init__(self):
    self.config = {}

  def init_build(self, thread_num):
    self.mark_dict = RecordDict("mark_dict.yaml")
    self.header_depend = RecordDict("header_depend.yaml")
    self.compile_commands = CompileCommands("compile_commands.json")
    self.thread_pool = ThreadPool(thread_num)

env = Env()

def batch(tasks):
  return env.thread_pool.batch(tasks)

def get_config():
  return env.config

def read_config(env):
  try:
    config_mtime, config_content = read_yaml("./mcons_config.yaml")
    if config_content["mcons_version"] != "1.0.1":
      print("mcons_config.yaml version mismatch, please run")
      print(sys.argv[0] + " init")
      exit(1)
    else:
      env.config = config_content["config"]
  except:
    print("mcons_config.yaml not found, please run")
    print(sys.argv[0] + " init")
    exit(1)

def save_config(env, defs):
  for pair in defs:
    p = pair.split("=", 1)
    value = True if len(p) == 1 else p[1]
    env.config[p[0]] = value
  
  config_content = {"mcons_version": "1.0.1", "config": env.config}
  save_yaml("mcons_config.yaml", config_content)()
