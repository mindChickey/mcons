
import argparse

from .act_build import build, count
from .run_init import put_defs
from .env import env
from .fuze_file import read_fuze

def add_build_argv(build_parser):
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")
  build_parser.add_argument("-p", "--print-command", action='store_true', help="print command")
  build_parser.add_argument("-q", "--quiet", action='store_true', help="don't print message")
  build_parser.add_argument("-D", action='append', metavar="KEY[=VALUE]", help="define key value pair")

def parse_jobs(jobs):
  if jobs == None:
    return None
  try:
    return int(jobs)
  except:
    print("jobs option error:", jobs)
    exit(1)

def run_build(cons):
  def f(args: argparse.Namespace):
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    config = read_fuze(args.fuze_file)
    put_defs(config, args.D)
    rule = cons(config)
    invalid_num = count(rule)
    build(rule, invalid_num, args.print_command, args.quiet)
  return f

def reg_build_mode(subparsers, cons):
  func = run_build(cons)
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)