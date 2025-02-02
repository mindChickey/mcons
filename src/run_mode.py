
import sys
import argparse

from .env import env, save_config
from .parse_args import parse_args
from .run_clean import run_clean
from .run_build import run_build
from .run_watch import run_watch

def run_init(args: argparse.Namespace, default_config):
  defs = [] if args.D == None else args.D
  env.config = default_config
  save_config(env, defs)

def run_cons(pyfile, cons, argv=None, default_config={}):
  argv1 = argv if argv else sys.argv[1:]
  args = parse_args(argv1)
  mode = args.mode
  if mode == "init":
    run_init(args, default_config)
  elif mode == "build":
    run_build(cons, args)
  elif mode == "watch":
    run_watch(pyfile, args, argv1)
  elif mode == "clean":
    run_clean()
