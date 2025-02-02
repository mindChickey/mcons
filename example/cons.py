#!/usr/bin/python3

from mcons import batch, cons_object, format_command, task, ConsModule, init_mode, clean_mode, run, build_mode
from bbb.bbb_cons import cons_bbb_a, compile_templ

cm = ConsModule(__file__)

def cons_main_o():
  return cons_object(cm, "main.c", "main.o", compile_templ)

def cons_main_exe():
  cmd = format_command("clang {0} {1} -o main")
  deps = batch([cons_main_o, cons_bbb_a])
  return task(cm, "main", deps, cmd)

if __name__ == "__main__":
  modes = [
    init_mode({"FLAGS": "-O3"}),
    build_mode(cons_main_exe),
    # watch_mode(__file__),
    clean_mode()
  ]
  run(modes)
