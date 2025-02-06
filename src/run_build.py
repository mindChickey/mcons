
import argparse

from .cons_module import ConsModule
from .env import env
from .config import read_config

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

def build_rule(cm: ConsModule, name: str, build_func):
  target = cm.target(name)
  return build_func(cm, target)

def run_build(cons):
  def f(args: argparse.Namespace):
    read_config()
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    env.rule = build_rule
    cons()
  return f

def reg_build_mode(subparsers, cons):
  func = run_build(cons)
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)