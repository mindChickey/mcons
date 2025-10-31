
from mcons import object_list, pack_ar, ConsModule

cm = ConsModule(__file__)

def cons_bbb_a(config):
  cmd = "gcc -c {_deps} -o {_target} " + config["FLAGS"]
  objs = object_list(cm, ".o", ["bbb.c", "ccc.c"], cmd)
  return pack_ar(cm, "libBBB.a", objs)
