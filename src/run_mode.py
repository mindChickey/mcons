
import argparse

from .parse_args import parse_args
from .core import clean_all, watch
from .config import save_config, read_config

def run_init(args: argparse.Namespace):
  defs = [] if args.D == None else args.D
  save_config(defs)

def run_build(cons, args: argparse.Namespace):
  read_config()
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
