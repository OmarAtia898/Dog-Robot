from bluedot.btcomm import BluetoothServer
from signal import pause
import RPi.GPIO as GPIO     # Import Library to access GPIO PIN
import time                 # To access delay function
GPIO.setwarnings(False)     # To avoid same PIN use warning
GPIO.setmode(GPIO.BOARD)    # Consider complete raspberry-pi board
LED_PIN_1 = 7                 # Define PIN for LED
LED_PIN_2 = 11                 # Define PIN for LED
IR_PIN = 13                 # Define PIN for IR Sensor
GPIO.setup(LED_PIN_1,GPIO.OUT)   # Set pin function as output
GPIO.setup(LED_PIN_2,GPIO.OUT)   # Set pin function as output
GPIO.setup(IR_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)   # Set pin function as input
GPIO.output(LED_PIN_2,GPIO.HIGH)  #LED OFF
GPIO.output(LED_PIN_1,GPIO.HIGH)  #LED OFF
def data_received(data):
    print(data)
    if(data == "led1_ON"):
        GPIO.output(LED_PIN_1,GPIO.LOW)  #LED ON
    elif(data == "led1_OFF"):
        GPIO.output(LED_PIN_1,GPIO.HIGH)  #LED OFF
    elif(data == "led2_ON"):
        GPIO.output(LED_PIN_2,GPIO.LOW)  #LED ON
    elif(data == "led2_OFF"):
        GPIO.output(LED_PIN_2,GPIO.HIGH)  #LED OFF
    else:
        GPIO.output(LED_PIN_2,GPIO.HIGH)  #LED OFF
        GPIO.output(LED_PIN_1,GPIO.HIGH)  #LED OFF
        
s = BluetoothServer(data_received)  #Received data from bluetooth
pause()
