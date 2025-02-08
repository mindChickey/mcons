
import argparse
from threading import Lock

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

def count(rule: Rule):
  if isinstance(rule, SourceRule):
    return 0
  else:
    invalids = batch_map(count, rule.deps)
    valid = rule.check_func()
    s = 0 if valid else 1
    return s + sum(invalids)

def build(root_rule: Rule, invalid_num):
  rank = 0
  lock = Lock()
  def print_message(filepath):
    nonlocal rank
    with lock:
      progress = f"[{rank}/{invalid_num}] "
      color_filepath = f"\033[32;1m{filepath}\033[0m"
      print(progress + color_filepath)
      rank = rank + 1

  def build1(rule: Rule):
    if isinstance(rule, TargetRule):
      batch_map(build1, rule.deps)
      if not rule.valid:
        print_message(rule.filepath)
        rule.build_func()
        return rule

  build1(root_rule)
  print("finish")

def run_build(cons):
  def f(args: argparse.Namespace):
    read_config()
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    rule = cons()
    invalid_num = count(rule)
    build(rule, invalid_num)
  return f

def reg_build_mode(subparsers, cons):
  func = run_build(cons)
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)