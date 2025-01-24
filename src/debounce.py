
import threading
import time

class DebounceThread:
  def __init__(self, delay):
    self.delay = delay
    self.last_task = lambda: None
    self.target_time = 0
    self.thread = threading.Thread(target=self.debounce)
    self.thread.daemon = True
    self.thread.start()

  def debounce(self):
    current_time = time.time()
    while True:
      target_time0 = self.target_time
      diff = target_time0 - current_time
      if diff < 0:
        time.sleep(self.delay)
        current_time = current_time + self.delay
      else:
        time.sleep(diff)
        if target_time0 == self.target_time:
          self.last_task()
          current_time = time.time()
        else:
          current_time = target_time0

  def dispose(self, task):
    self.last_task = task
    self.target_time = time.time() + self.delay
  
  def thread_join(self):
    self.thread.join()

debounce = DebounceThread(1)

while True:
  r = input()
  debounce.dispose(lambda: print(r))
