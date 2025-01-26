
import argparse

from .parse_args import parse_args
from .core import clean_all, watch

init_env = {}

def run_init(args: argparse.Namespace):
  for pair in args.D:
    p = pair.split("=", 1)
    init_env[p[0]] = True if len(p) == 1 else p[1]
  print(init_env)

def run_build(cons, args: argparse.Namespace):
  cons()

def run_watch(pyfile, args: argparse.Namespace):
  watch(pyfile, args.R)

def run_clean(args):
  clean_all()
  
def run_cons(pyfile, cons, argv=None):
  args = parse_args(argv)
  mode = args.mode
  if mode == "init":
    run_init(args)
  elif mode == "build":
    run_build(cons, args)
  elif mode == "watch":
    run_watch(pyfile, args)
  elif mode == "clean":
    run_clean(args)
