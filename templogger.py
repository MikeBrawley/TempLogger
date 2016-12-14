import RPi.GPIO as GPIO
import os
import glob
import time
import thread
from ISStreamer.Streamer import Streamer

# -------- User Settings ------------
BUCKET_NAME = "your_bucket_name"    	#Your Initial State Bucket Name
BUCKET_KEY = "your_bucket_key"    	# your Initial State Bucket Key
ACCESS_KEY = "your_access_key"  	# your Access Key for InitialState.com
STREAM_NAME= "your_stream_name" 	# The name of this temperature sensor
INTERVAL = 300				# The interval you want to pull temp in seconds
# ----------------------------


GPIO_SWITCH_PIN = 21  #GPIO pin for off switch
GPIO_LED_PIN = 18  #GPIO pin for the script LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PGIO_LED_PIN,GPIO.OUT)
GPIO.setup(GPIO_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def stream_temp(streamer):
    while True:
        temp_c = read_temp()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        streamer.log(STREAM_NAME, temp_f)
        streamer.flush()
        time.sleep(INTERVAL)

	
def main():
    streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    # Start temperature stream thread
    try:
        thread.start_new_thread(stream_temp, (streamer, ))
	GPIO.output(GPIO_LED_PIN,GPIO.HIGH)
    except:
        print "Error: unable to start temperature streamer thread"
        pass
	# Button
    try:
        ## if button is pressed
        GPIO.wait_for_edge(GPIO_SWITCH_PIN, GPIO.FALLING)
        os.system("sudo shutdown -h now")
    except:
        pass
    GPIO.cleanup()
	
if __name__ == "__main__":
    main()    
