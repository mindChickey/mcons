#!/usr/bin/python3

from mcons import batch, cons_object, format_command, need_update, task, ConsModule, clean_all
from bbb.bbb_cons import cons_bbb_a, compile_templ

cm = ConsModule(__file__)

def cons_main_o():
  return cons_object(cm, "main.c", "main.o", compile_templ)

def cons_main_exe():
  cmd = format_command("clang {0} {1} -o main")
  deps = batch([cons_main_o, cons_bbb_a])
  return task(cm, "main", deps, cmd)

if __name__ == "__main__":
  r =  cons_main_exe()
  print(r)
