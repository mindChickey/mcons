
from threading import Lock

from ..rules.rule import Rule, TravelStatus, TargetRule
from ..core.env import batch_map

def travel_rule(rule, status, default_ret, func):
  if isinstance(rule, TargetRule):
    with rule.lock:
      if rule.travel_status == status:
        return default_ret
      else:
        rule.travel_status = status
        return func(rule)
  else:
    return default_ret

def count1(rule: TargetRule):
  invalids = batch_map(count, rule.deps)
  valid = rule.check_func()
  s = 0 if valid else 1
  return s + sum(invalids)

def count(rule: Rule):
  return travel_rule(rule, TravelStatus.HasCount, 0, count1)

def build(root_rule: Rule, invalid_num, print_command, quiet):
  rank = 0
  lock = Lock()
  def print_message(rule):
    nonlocal rank
    if quiet: return
    with lock:
      progress = f"[{rank}/{invalid_num}] "
      print(progress + rule.get_message(print_command))
      rank = rank + 1

  def build0(rule: TargetRule):
    batch_map(build1, rule.deps)
    if not rule.valid:
      print_message(rule)
      rule.build_func()
      return rule

  def build1(rule: Rule):
    return travel_rule(rule, TravelStatus.HasBuild, rule, build0)

  build1(root_rule)
  print(f"\033[32;1mfinish\033[0m")