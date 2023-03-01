import subprocess

# def run_parallel(commands, nproc):

#     n = nproc #the number of parallel processes you want
#     for j in range(max(int(len(commands)/n), 1)):
#         procs = [subprocess.Popen(i, shell=True) for i in commands[j*n: min((j+1)*n, len(commands))] ]
#         for p in procs:
#             p.wait()

##
# or maybe use a queue like shown here
import queue
import threading

commands = ["cellpose", "jupyter notebook", "code .", "cellpose"]

q = queue.Queue()
result = {}  # used to store the results
for command in commands:
  q.put(command)

def worker():
  while True:
    command = q.get()
    if command is None:  # Sentinel?
      return
    subprocess.call(command, shell=True)

    # result[fileName] = checksum  # store it

threads = [ threading.Thread(target=worker) for _i in range(4) ]
for thread in threads:
  thread.start()
  q.put(None)  # one Sentinel marker for each thread