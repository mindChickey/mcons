
import argparse

from .env import env, save_config

def run_init(default_config):
  def f(args: argparse.Namespace):
    defs = [] if args.D == None else args.D
    env.config = default_config
    save_config(env, defs)
  return f

def reg_init_mode(subparsers, default_config):
  func = run_init(default_config)
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  init_parser.set_defaults(func=func)