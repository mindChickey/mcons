
from mcons import pack_ar, ConsModule, rule

cm = ConsModule(__file__)

compile_templ = "clang {FLAGS} -c {0} -o {1}"

def cons_bbb_a():
  return rule(cm, "libBBB.a", pack_ar(["bbb.c", "ccc.c"], compile_templ))
