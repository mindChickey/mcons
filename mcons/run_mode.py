
import argparse
from .run_init  import reg_init_mode
from .run_clean import reg_clean_mode
from .run_build import reg_build_mode
from .run_watch import reg_watch_mode

def make_parser(file, cons, default_config, reg_custom_modes):
  parser = argparse.ArgumentParser()
  parser.add_argument("fuze_file", type=str, nargs='?', default='mcons_fuze', help="fuze file")

  sp = parser.add_subparsers()
  reg_init_mode(sp, file, default_config)
  reg_build_mode(sp, cons)
  reg_watch_mode(sp, file)
  reg_clean_mode(sp, cons)
  [f(sp) for f in reg_custom_modes]
  return parser

def parse_args(parser, argv=None):
  args = parser.parse_args(argv)
  if hasattr(args, 'func'):
    return args
  else:
    parser.print_help()
    exit(0)

def run_cons(file, cons, default_config={}, argv=None, reg_custom_modes=[]):
  parser = make_parser(file, cons, default_config, reg_custom_modes)
  args = parse_args(parser, argv)
  return args.func(args)
