
import os
import sys

from .record_dict import read_yaml, save_yaml
from .env import env

def read_config():
  try:
    config_mtime, config_content = read_yaml(env.config_filename)
    if config_content["mcons_version"] != "1.0.2":
      print("mcons_config.yaml version mismatch, please run")
      print(sys.argv[0] + " init")
      exit(1)
    else:
      return config_content["config"]
  except:
    print("mcons_config.yaml not found, please run")
    print(sys.argv[0] + " init")
    exit(1)

def save_config(cons_file: str, config_dict):
  config_content = {
    "mcons_version": "1.0.2", 
    "cons_file": os.path.abspath(cons_file),
    "config": config_dict
  }
  save_yaml(env.config_filename, config_content)()
