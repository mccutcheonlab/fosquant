import subprocess as sub
import threading

import queue

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

q = queue.Queue()
result = {}  # used to store the results
for command in commands:
  q.put(command)

def worker():
  while True:
    command = q.get()
    if command is None:  # Sentinel?
      return
    RunCmd(["python"], 5).Run() # add command


threads = [ threading.Thread(target=worker) for _i in range(4) ]
for thread in threads:
  thread.start()
  q.put(None)  # one Sentinel marker for each thread

if __name__ == "__main__":
    RunCmd(["python"], 5).Run()
