
from mcons import pack_ar, ConsModule

cm = ConsModule(__file__)

compile_templ = "clang -c {0} -o {1}"

cons_bbb_a = pack_ar(cm, "libBBB.a", ["bbb.c", "ccc.c"], compile_templ)