import threading
import time
import datetime
import RPi.GPIO as GPIO 
import Helper


from IMU import *
from picamera import PiCamera
from Helper import *
from scipy import ndimage
from scipy import misc

log = LogHelper()

log.logInfo('Data capturing started...')
log.logInfo('******************************************************')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
imu = IMU()

def worker():
    imu.read()

try:
    command = ''
    camera = PiCamera()

    while (True):
        
        #if(command == 'y'):
            #command = ''
        if(GPIO.input(17)):
            
            thread = threading.Thread(target=worker)
           
            log.logInfo('Button press detected...')
            log.logInfo('=====================================================')

            imu.startrec()
            
            thread.start()             
            
            #Wait 200 ms to start data capturing, enabling sensors to initialise
            time.sleep(0.2)

            camera.start_preview()

            log.logInfo('Camera started...')

            i = datetime.datetime.now()  
			timestmp = str(i).replace(":",".");
            imagefile = "/home/pi/source/DC/Files/Image_"+ timestmp + ".jpg"
            camera.capture(imagefile)

            log.logInfo('Image captured and saved to '  + imagefile)

            camera.stop_preview()

            log.logInfo('Camera stopped...')
            
            imu.stoprec()

            datafile = "/home/pi/source/DC/Files/SensorData_"+ timestmp + ".txt"
                        
            f= open(datafile,"w+")
            for i in imu.DATA:
                f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s \n' % (str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]),str(i[7]),str(i[8]),str(i[9])))
            f.close()

			image = misc.imread(imagefile)
            rotate_image = ndimage.rotate(image, 180) 
			misc.imsave(imagefile, rotate_image)
            log.logInfo("Data captured and saved to  " + datafile)
        #else:             
            #command = raw_input('Do you want to take a photo y/n ? ')
            #if command == 'y':
                #continue;
            #else:
                #sys.exit();
except Exception:
    log.logError("Error in capturing data") 


log.logInfo('End of main thread')
log.logInfo('*************************************************')
