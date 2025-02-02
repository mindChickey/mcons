
import sys
import argparse
from os import path
from watchrun import watch_dir_cmds

from .run_build import add_build_argv

"""
def add_watch_command(subparsers, func):
  watch_parser = subparsers.add_parser("watch", help="watch mode")
  add_build_argv(watch_parser)
  watch_parser.add_argument("-R", action='append', metavar="command", help="run command")
  watch_parser.set_defaults(func=func)

def get_build_argv(argv):
  argv1 = []
  for arg in argv[1:]:
    if not arg.startswith("-D"):
      argv1.append(arg)
  return argv1
  
def watch(pyfile, cmds):
  src_dir = path.dirname(pyfile)
  build_dir = path.curdir
  watch_dir_cmds(src_dir, 1, cmds, [build_dir], run_now=True)

def run_watch(pyfile, args: argparse.Namespace, argv):
  cmds = [] if args.R == None else args.R
  build_argv = get_build_argv(argv)
  build_cmd = f"{sys.executable} {pyfile} build " + ' '.join(build_argv)
  watch(pyfile, [build_cmd] + cmds)

def watch_mode(pyfile):
  def f(subparsers):
    add_watch_command(subparsers, run_watch(default_config))
  return f
"""