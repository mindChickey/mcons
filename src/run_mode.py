
import sys
import argparse

from .env import env, save_config, read_config
from .parse_args import parse_args
from .core import clean_all, watch

def run_init(args: argparse.Namespace, default_config):
  defs = [] if args.D == None else args.D
  env.config = default_config
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

def get_build_argv(argv):
  argv1 = []
  for arg in argv[1:]:
    if not arg.startswith("-D"):
      argv1.append(arg)
  return argv1

def run_watch(pyfile, args: argparse.Namespace, argv):
  cmds = [] if args.R == None else args.R
  build_argv = get_build_argv(argv)
  watch(pyfile, build_argv, cmds)

def run_clean(args):
  clean_all()
  
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
    run_clean(args)
