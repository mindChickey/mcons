
from os import path, remove

from .record_dict import read_yaml
from .env import env

def remove_file(name):
  try:
    remove(name)
  except:
    None

def run_clean():
  mtime, mark_dict = read_yaml(env.mark_dict_filename)
  remove_file(env.mark_dict_filename)
  remove_file(env.header_depend_filename)
  remove_file(env.compile_commands_filename)

  for name in mark_dict.keys():
    remove_file(name)
