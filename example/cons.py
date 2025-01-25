#!/usr/bin/python3

import sys
from mcons import batch, cons_object, format_command, need_update, task, ConsModule, clean_all, watch
from bbb.bbb_cons import cons_bbb_a, compile_templ

cm = ConsModule(__file__)

def cons_main_o():
  return cons_object(cm, "main.c", "main.o", compile_templ)

def cons_main_exe():
  cmd = format_command("clang {0} {1} -o main")
  deps = batch([cons_main_o, cons_bbb_a])
  return task(cm, "main", deps, cmd)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    r =  cons_main_exe()
    print(r)
  elif sys.argv[1] == "--watch":
    watch(__file__, sys.argv[2:])
