#!/usr/bin/python3

import argparse

init_env = {}

def run_init(cons, args: argparse.Namespace):
  for pair in args.D:
    p = pair.split("=", 1)
    init_env[p[0]] = True if len(p) == 1 else p[1]
  print(init_env)

def add_init_command(subparsers):
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  init_parser.set_defaults(func=run_init)

def run_build(cons, args: argparse.Namespace):
  cons()

def add_build_command(subparsers):
  build_parser = subparsers.add_parser("build", help="build project")
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  build_parser.set_defaults(func=run_build)

def run_watch(cons, args: argparse.Namespace):
  print(args)

def add_watch_command(subparsers):
  watch_parser = subparsers.add_parser("watch", help="watch mode")
  watch_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  watch_parser.add_argument("-R", action='append', metavar="command", help="run command")
  watch_parser.set_defaults(func=run_watch)

def parse_args(argv=None):
  parser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers()
  add_init_command(subparsers)
  add_build_command(subparsers)
  add_watch_command(subparsers)
  args = parser.parse_args(argv)

  if not hasattr(args, 'func'):
    parser.print_help()
    exit(0)
  else:
    return args

def run_cons(cons, argv=None):
  args = parse_args(argv)
  args.func(cons, args)