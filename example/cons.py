#!/usr/bin/python3

from mcons import cons_object, format_command, task, ConsModule
from bbb.bbb_cons import cons_bbb_a, compile_templ

cm = ConsModule(__file__)

cons_main_o = cons_object(cm, "main.c", "main.o", compile_templ)

cons_main_exe = task(cm, "main", [cons_main_o, cons_bbb_a],
  format_command("clang {0} {1} -o main")
)

if __name__ == "__main__":
  r =  cons_main_exe()
  print(r)
