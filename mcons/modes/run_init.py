
import argparse
from ..metafile.fuze_file import save_fuze

def put_defs(config, D):
  defs = [] if D == None else D
  for pair in defs:
    p = pair.split("=", 1)
    value = True if len(p) == 1 else p[1]
    config[p[0]] = value

def run_init(cons_file: str, default_config):
  def f(args: argparse.Namespace):
    config = default_config
    put_defs(config, args.D)
    save_fuze(args.fuze_file, cons_file, config)
  return f

def reg_init_mode(subparsers, cons_file, default_config={}):
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  func = run_init(cons_file, default_config)
  init_parser.set_defaults(func=func)