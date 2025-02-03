
from os import remove

from .record_dict import read_yaml
from .env import env

def remove_file(name):
  try:
    remove(name)
  except:
    None

def run_clean(args):
  mtime, mark_dict = read_yaml(env.mark_dict_filename)
  remove_file(env.mark_dict_filename)
  remove_file(env.header_depend_filename)
  remove_file(env.compile_commands_filename)

  for name in mark_dict.keys():
    remove_file(name)

def reg_clean_mode(subparsers):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  watch_parser.set_defaults(func=run_clean)
