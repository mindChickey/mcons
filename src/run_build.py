
import argparse

from .env import env, read_config

def add_build_argv(build_parser):
  build_parser.add_argument("-j", "--jobs", metavar="N", help="allow N jobs")

def add_build_command(subparsers, func):
  build_parser = subparsers.add_parser("build", help="build project")
  add_build_argv(build_parser)
  build_parser.set_defaults(func=func)

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
    read_config(env)
    thread_num = parse_jobs(args.jobs)
    env.init_build(thread_num)
    cons()
  return f

def build_mode(cons):
  def f(subparsers):
    add_build_command(subparsers, run_build(cons))
  return f