
import sys
from .record_dict import read_yaml, save_yaml

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

def save_config(defs):
  global config
  for pair in defs:
    p = pair.split("=", 1)
    value = True if len(p) == 1 else p[1]
    config[p[0]] = value
  
  config_content = {"mcons_version": "1.0.1", "config": config}
  save_yaml("mcons_config.yaml", config_content)()
