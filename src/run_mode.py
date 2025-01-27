
import sys
import argparse

from .record_dict import read_yaml, save_yaml
from .parse_args import parse_args
from .core import clean_all, watch

config = {}

def get_config():
  return config

def read_config():
  global config
  try:
    config_mtime, config_content = read_yaml("./mcons_config.yaml")
    if config_content["mcons_version"] != "1.0.1":
      print("mcons_config.yaml version mismatch, please run")
      print(sys.argv[0] + " init")
      exit(1)
    else:
      config = config_content["config"]
  except:
    print("mcons_config.yaml not found, please run")
    print(sys.argv[0] + " init")
    exit(1)

def run_init(args: argparse.Namespace):
  global config
  for pair in args.D:
    p = pair.split("=", 1)
    config[p[0]] = True if len(p) == 1 else p[1]
  
  config_content = {"mcons_version": "1.0.1", "config": config}
  save_yaml("mcons_config.yaml", config_content)()

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
