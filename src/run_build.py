
import argparse

from .env import batch_map, env
from .config import read_config
from .cons_module import Rule, SourceRule, TargetRule

def add_build_argv(build_parser):
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")

def parse_jobs(jobs):
  if jobs == None:
    return None
  try:
    return int(jobs)
  except:
    print("jobs option error:", jobs)
    exit(1)

def build(rule: Rule):
  if isinstance(rule, TargetRule):
    batch_map(build, rule.deps)
    rule.build_func()
    return rule

def run_build(cons):
  def f(args: argparse.Namespace):
    read_config()
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    rule = cons()
    build(rule)
  return f

def reg_build_mode(subparsers, cons):
  func = run_build(cons)
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)