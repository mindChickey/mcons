
import argparse

from .env import env, save_config, read_config
from .parse_args import parse_args
from .core import clean_all, watch

def run_init(args: argparse.Namespace):
  defs = [] if args.D == None else args.D
  save_config(env, defs)

def parse_jobs(jobs):
  if jobs == None:
    return None
  try:
    return int(jobs)
  except:
    print("jobs option error:", jobs)
    exit(1)

def run_build(cons, args: argparse.Namespace):
  read_config(env)
  thread_num = parse_jobs(args.jobs)
  env.init_build(thread_num)
  cons()

def run_watch(pyfile, args: argparse.Namespace):
  cmds = [] if args.R == None else args.R
  watch(pyfile, cmds)

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
