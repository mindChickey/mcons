#!/usr/bin/python3

from mcons import batch, object, task, ConsModule, run_cons
from bbb.bbb_cons import cons_bbb_a

cm = ConsModule(__file__)

def cons_main_o(config):
  cmd = "gcc -c {0} -o {_target} " + config["FLAGS"]
  return object(cm, "main.o", "main.c", cmd)

def cons_main_exe(config):
  deps = batch([cons_main_o, cons_bbb_a], config)
  cmd = "clang {_deps} -o {_target}"
  return task(cm, "main", deps, cmd)

default_config = {"FLAGS": "-O3"}

if __name__ == "__main__":
  run_cons(__file__, cons_main_exe, default_config)
