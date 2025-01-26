#!/usr/bin/python3

import argparse

def add_init_command(subparsers):
  init_parser = subparsers.add_parser("init", help="init args")
  init_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")
  init_parser.set_defaults(mode="init")

def add_build_command(subparsers):
  build_parser = subparsers.add_parser("build", help="build project")
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  build_parser.set_defaults(mode="build")

def add_watch_command(subparsers):
  watch_parser = subparsers.add_parser("watch", help="watch mode")
  watch_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  watch_parser.add_argument("-R", action='append', metavar="command", help="run command")
  watch_parser.set_defaults(mode="watch")

def add_clean_command(subparsers):
  watch_parser = subparsers.add_parser("clean", help="clean mode")
  watch_parser.set_defaults(mode="clean")

def parse_args(argv=None):
  parser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers()
  add_init_command(subparsers)
  add_build_command(subparsers)
  add_watch_command(subparsers)
  add_clean_command(subparsers)
  # add_custom_command(subparsers)
  args = parser.parse_args(argv)

  if not hasattr(args, 'mode'):
    parser.print_help()
    exit(0)
  else:
    return args
