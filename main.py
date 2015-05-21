__author__ = 'Terrace Boiz'

import mbtaJsonParse
import Weather
import Queue
import threading

files = [mbtaJsonParse, Weather]
q = Queue.Queue()

def runMain(q, file):
    q.put(file.main())

if __name__ == "__main__":
    for f in files:
        t = threading.Thread(target=runMain, args = (q, f))
        t.daemon = True
        t.start()

    s = q.get()
    print s



