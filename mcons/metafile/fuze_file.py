
import os
import sys
import yaml

from .record_dict import read_yaml

def read_fuze(fuze_file):
  try:
    fuze_mtime, fuze_content = read_yaml(fuze_file)
    if fuze_content["mcons_version"] != "1.0.5":
      print(fuze_file + " version mismatch, please run")
      print(sys.argv[0] + " init")
      exit(1)
    else:
      return fuze_content["config"]
  except:
    print(fuze_file + " not found, please run")
    print(sys.argv[0] + " init")
    exit(1)

def save_fuze(fuze_file, cons_file: str, config_dict):
  cons_file1 = os.path.abspath(cons_file)
  fuze_content = {
    "mcons_version": "1.0.5",
    "cons_file": cons_file1,
    "config": config_dict
  }
  with open(fuze_file, 'w', encoding='utf-8') as f:
    f.write(f"#!{sys.executable} {cons_file1}\n\n")
    yaml.dump(fuze_content, f)

  os.chmod(fuze_file, 0o755)
