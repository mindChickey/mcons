
import concurrent.futures
import atexit

class ThreadPool:
  def __init__(self):
    self.executor = concurrent.futures.ThreadPoolExecutor()
    atexit.register(lambda: self.executor.shutdown())

  def batch(self, tasks):
    futures = [self.executor.submit(task) for task in tasks]
    results = []
    i = len(tasks)
    while i > 0:
      index = i - 1
      if futures[index].cancel():
        results.append(tasks[index]())
        i = index
      else:
        break

    results0 = [future.result() for future in futures[0:i]]
    results.reverse()
    return results0 + results

thread_pool = ThreadPool()

def batch(tasks):
  return thread_pool.batch(tasks)
