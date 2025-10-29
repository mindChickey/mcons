
import os
import sys
import yaml

from .record_dict import read_yaml

def read_config(fuze_file):
  try:
    config_mtime, config_content = read_yaml(fuze_file)
    if config_content["mcons_version"] != "1.0.5":
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
  cons_file1 = os.path.abspath(cons_file)
  config_content = {
    "mcons_version": "1.0.5",
    "cons_file": cons_file1,
    "config": config_dict
  }
  with open("./mcons_fuze", 'w', encoding='utf-8') as f:
    f.write(f"#!{sys.executable} {cons_file1}\n\n")
    yaml.dump(config_content, f)

  os.chmod("./mcons_fuze", 0o755)
