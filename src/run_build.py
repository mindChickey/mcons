
import argparse

from .env import env, read_config

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
