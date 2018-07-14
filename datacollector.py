import threading;
from IMU import IMUTest

class threadTest(threading.Thread):
    def __init__(self, name):        
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print "Starting data collection " + self.name
        imu = IMUTest();
        imu.read();


#thread2 = threadTest("Thread 2")


#thread2.start()

print "Exiting main thread"
