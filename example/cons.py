#!/usr/bin/python3

from mcons import batch, object_rule, task, ConsModule, run_cons, reg_init_mode, reg_clean_mode, reg_build_mode, reg_watch_mode
from bbb.bbb_cons import cons_bbb_a

cm = ConsModule(__file__)

def cons_main_o(config):
  cmd = "gcc -c {0} -o {1} " + config["FLAGS"]
  return object_rule(cm, "main.c", "main.o", cmd)

def cons_main_exe(config):
  deps = batch([cons_main_o, cons_bbb_a], config)
  cmd = "clang {0} -o {1}"
  return task(cm, "main", deps, cmd)

default_config = {"FLAGS": "-O3"}

def reg_modes(sp):
  reg_init_mode(sp, __file__, default_config)
  reg_build_mode(sp, cons_main_exe)
  reg_watch_mode(sp, __file__)
  reg_clean_mode(sp, cons_main_exe)

if __name__ == "__main__":
  run_cons(reg_modes)
