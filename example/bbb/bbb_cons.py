
from mcons import pack_ar, ConsModule, rule

cm = ConsModule(__file__)

compile_templ = "clang {FLAGS} -c {0} -o {1}"

def cons_bbb_a():
  return pack_ar(cm, "libBBB.a", ["bbb.c", "ccc.c"], compile_templ)
