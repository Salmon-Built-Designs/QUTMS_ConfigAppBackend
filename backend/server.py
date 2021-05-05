import time
import threading
import sys
import time
from server_can_thread import thread_CAN

def thread_socket():
   print("Socket Start")

   
   while True:
      print("Socket")
      time.sleep(2)



class CANThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      print ("Starting " + self.name)
      thread_CAN()
      print ("Exiting " + self.name)

class SocketThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      print ("Starting " + self.name)
      thread_socket()
      print ("Exiting " + self.name)

def main():
    thread1 = CANThread(1, "CAN Thread")
    thread2 = SocketThread(2, "Socket Thread")

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Exiting main thread")


if __name__ == '__main__':
    main()