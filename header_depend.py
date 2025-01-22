
import atexit
import yaml

def read_yaml(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      return yaml.safe_load(f)
  except:
    return {}

def save_yaml(filename, depend_map):
  def f():
    with open(filename, 'w', encoding='utf-8') as f:
      yaml.dump(depend_map, f)
  return f

def openHeaderDependFile(filename):
  depend_map = read_yaml(filename)
  atexit.register(save_yaml(filename, depend_map))
  return depend_map

header_depend = openHeaderDependFile("header_depend.yaml")

def get_header_depend(obj):
  return header_depend.get(obj)

def update_header_depend(depfile):
  depfile.seek(0)
  content = depfile.read()
  r = content.split()
  obj = r[0][0:-1]
  deps = list(filter(lambda x: x != '\\', r[1:]))
  header_depend[obj] = deps
