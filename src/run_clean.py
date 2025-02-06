
from os import remove

from .record_dict import read_yaml
from .env import env

def remove_file(name):
  try:
    remove(name)
  except:
    None

def run_clean(extra_files):
  def f(args):
    mtime, mark_dict = read_yaml(env.mark_dict_filename)
    remove_file(env.mark_dict_filename)
    remove_file(env.header_depend_filename)
    remove_file(env.compile_commands_filename)

    for name in mark_dict.keys():
      remove_file(name)
    for name in extra_files:
      remove_file(name)
  return f

def reg_clean_mode(subparsers, extra_files=[]):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  watch_parser.set_defaults(func=run_clean(extra_files))
