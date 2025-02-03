#!/usr/bin/python3

from mcons import batch, cons_object, format_command, task, ConsModule, run, reg_init_mode, reg_clean_mode, reg_build_mode, reg_watch_mode
from bbb.bbb_cons import cons_bbb_a, compile_templ

cm = ConsModule(__file__)

def cons_main_o():
  return cons_object(cm, "main.c", "main.o", compile_templ)

def cons_main_exe():
  cmd = format_command("clang {0} {1} -o main")
  deps = batch([cons_main_o, cons_bbb_a])
  return task(cm, "main", deps, cmd)

def reg_modes(sp):
  reg_init_mode(sp, {"FLAGS": "-O3"}),
  reg_build_mode(sp, cons_main_exe),
  reg_watch_mode(sp, __file__),
  reg_clean_mode(sp)

if __name__ == "__main__":
  run(reg_modes)
