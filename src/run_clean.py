
from os import remove

from .cons_module import ConsModule
from .env import env

def remove_file(name):
  try:
    remove(name)
  except:
    None

def clean_rule(cm: ConsModule, name: str, build_func):
  target = cm.target(name)
  print("clean", target)
  remove_file(target.filepath)
  return target

def run_clean(cons, extra_files):
  def f(args):
    env.init_clean(None)
    remove_file(env.mark_dict_filename)
    remove_file(env.header_depend_filename)
    remove_file(env.compile_commands_filename)

    for name in extra_files:
      remove_file(name)

    env.rule = clean_rule
    cons()
  return f

def reg_clean_mode(subparsers, cons, extra_files=[]):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  watch_parser.set_defaults(func=run_clean(cons, extra_files))
