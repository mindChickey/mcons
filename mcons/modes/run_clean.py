
from os import remove

from ..metafile.fuze_file import read_fuze
from ..core.env import batch_map, env
from ..rules.rule import Rule, TargetRule

def remove_file(filepath):
  try:
    remove(filepath)
    print("clean", filepath)
  except:
    None

def clean(rule: Rule):
  if isinstance(rule, TargetRule):
    remove_file(rule.filepath)
    batch_map(clean, rule.deps)

def run_clean(cons, extra_files):
  def f(args):
    remove_file(env.mark_dict_filename)
    remove_file(env.header_depend_filename)
    remove_file(env.compile_commands_filename)

    for name in extra_files:
      remove_file(name)

    env.init_clean(None)
    config = read_fuze(args.fuze_file)
    rule = cons(config)
    clean(rule)
  return f

def reg_clean_mode(subparsers, cons, extra_files=[]):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  func = run_clean(cons, extra_files)
  watch_parser.set_defaults(func=func)
