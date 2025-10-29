
from mcons import cons_object_list, pack_ar, ConsModule

cm = ConsModule(__file__)

def cons_bbb_a(config):
  cmd = "gcc -c {0} -o {1} " + config["FLAGS"]
  objs = cons_object_list(cm, ["bbb.c", "ccc.c"], ".o", cmd)
  return pack_ar(cm, "libBBB.a", objs)
