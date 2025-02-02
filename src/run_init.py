
import argparse

from .env import env, save_config

def add_init_command(subparsers, func):
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  init_parser.set_defaults(func=func)

def run_init(default_config):
  def f(args: argparse.Namespace):
    defs = [] if args.D == None else args.D
    env.config = default_config
    save_config(env, defs)
  return f

def init_mode(default_config):
  def f(subparsers):
    add_init_command(subparsers, run_init(default_config))
  return f
  