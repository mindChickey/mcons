
from mcons import pack_ar, ConsModule, clean_files

cm = ConsModule(__file__)

compile_templ = "clang -c {0} -o {1}"

def cons_bbb_a():
  return pack_ar(cm, "libBBB.a", ["bbb.c", "ccc.c"], compile_templ)

def clean():
  clean_files(cm, ["bbb.o", "ccc.o", "libBBB.a"])