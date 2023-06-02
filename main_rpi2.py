import socket
import pickle
import time
import RPi.GPIO as GPIO
from bluedot.btcomm import BluetoothServer
from signal import pause


bluetooth_data = ""
temp_data = ""
def data_received(data):
  print("Data: ", data)
  global bluetooth_data
  bluetooth_data = data

def getReceivedData():
  return bluetooth_data


def client_connected():
    print("client connected")

def client_disconnected():
    print("client disconnected")

def PrintInfo():
  print("-----------------------")
  print("Choose an option below")
  print("0 - Exit Bluetooth Mode")
  print("1 - Turn Right")
  print("2 - Turn Left")
  print("3 - Stand Up")
  print("4 - Sit")
  print("5 - Go Forward")
  print("6 - Go Backward")

def SetPwmForGpio(pin_no):
    GPIO.setup(pin_no,GPIO.OUT)
    servoNo = GPIO.PWM(pin_no,50) # pin 11 for servo1
    servoNo.start(0)
    time.sleep(1)
    return servoNo

def ExecuteServo(servoNo, angle):
    dutyCycle = angle / 18 + 2
    servoNo.ChangeDutyCycle(dutyCycle)
    time.sleep(0.5)
    # servoNo.ChangeDutyCycle(7.5)

def map_range(number, from_min, from_max, to_min, to_max):
    # Giriş aralığındaki sayıyı hedef aralığa map etmek için bir fonksiyon
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled = float(number - from_min) / float(from_range)
    return to_min + (scaled * to_range)

def DoMovement(servoList, angle):
  for servo in servoList:
     ExecuteServo(servo, angle)

def map_numbers(number):
    mapped_number = map_range(number, 250, 500, 90, 180)
    return mapped_number

resultImage = "omar"
currentname = "unknown"
encodingsP = "encodings.pickle"

GPIO.setmode(GPIO.BOARD)

redPin = 33
bluePin = 35
whitePin = 37

GPIO.setup(redPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(bluePin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(whitePin, GPIO.OUT, initial=GPIO.LOW)

# PWM PINS 7-11-12-13-15-16-18-22
servo1 = SetPwmForGpio(7)
servo2 = SetPwmForGpio(11)
# servo3 = SetPwmForGpio(12)
# servo4 = SetPwmForGpio(13)
# servo5 = SetPwmForGpio(15)
# servo6 = SetPwmForGpio(16)
# servo7 = SetPwmForGpio(18)
# servo8 = SetPwmForGpio(22)


print("Baglanti bekleniyor!")
GPIO.output(whitePin, GPIO.HIGH)
s = socket.socket()
 
port = 12345
 
s.bind(('', port))
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(1)    
c, addr = s.accept()
# close the socket connection
try:
  while True:
    getData = c.recv(1024).decode() 
    
    if "turn right" in getData:
      # servoList = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
      servoList = [servo1, servo2]
      DoMovement(servoList, 180)
      time.sleep(1.5)
    
    elif "turn left" in getData:      
      # servoList = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
      servoList = [servo1, servo2]
      DoMovement(servoList, 0)
      time.sleep(1.5)

    elif "stand up" in getData:
      # servoList = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
      servoList = [servo1, servo2]
      DoMovement(servoList, 180)
      time.sleep(1.5)

    elif "sit" in getData:      
      # servoList = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
      servoList = [servo1, servo2]
      DoMovement(servoList, 0)
      time.sleep(1.5)

    elif "go forward" in getData:
      for i in range(5):
        ExecuteServo(servo1, 180)
        ExecuteServo(servo2, 180)
        # ExecuteServo(servo3, 0)
        # ExecuteServo(servo4, 0)
        # ExecuteServo(servo5, 180)
        # ExecuteServo(servo6, 180)
        # ExecuteServo(servo7, 0)
        # ExecuteServo(servo8, 0)
        time.sleep(1)
        ExecuteServo(servo1, 0)
        ExecuteServo(servo2, 0)
        # ExecuteServo(servo3, 180)
        # ExecuteServo(servo4, 180)
        # ExecuteServo(servo5, 0)
        # ExecuteServo(servo6, 0)
        # ExecuteServo(servo7, 180)
        # ExecuteServo(servo8, 180)
        time.sleep(1)

    elif "go backward" in getData:
      for i in range(5):
        ExecuteServo(servo1, 0)
        ExecuteServo(servo2, 0)
        # ExecuteServo(servo3, 180)
        # ExecuteServo(servo4, 180)
        # ExecuteServo(servo5, 0)
        # ExecuteServo(servo6, 0)
        # ExecuteServo(servo7, 180)
        # ExecuteServo(servo8, 180)
        time.sleep(1)
        ExecuteServo(servo1, 180)
        ExecuteServo(servo2, 180)
        # ExecuteServo(servo3, 0)
        # ExecuteServo(servo4, 0)
        # ExecuteServo(servo5, 180)
        # ExecuteServo(servo6, 180)
        # ExecuteServo(servo7, 0)
        # ExecuteServo(servo8, 0)
        time.sleep(1)

    elif "follow me" in getData:
      GPIO.output(bluePin, GPIO.LOW)
      GPIO.output(redPin, GPIO.HIGH)
      for j in range(10):
        if j < 7:
            ExecuteServo(servo1, 180)
            ExecuteServo(servo2, 180)
            # ExecuteServo(servo3, 0)
            # ExecuteServo(servo4, 0)
            # ExecuteServo(servo5, 180)
            # ExecuteServo(servo6, 180)
            # ExecuteServo(servo7, 0)
            # ExecuteServo(servo8, 0)
            time.sleep(1)
            ExecuteServo(servo1, 0)
            ExecuteServo(servo2, 0)
            # ExecuteServo(servo3, 180)
            # ExecuteServo(servo4, 180)
            # ExecuteServo(servo5, 0)
            # ExecuteServo(servo6, 0)
            # ExecuteServo(servo7, 180)
            # ExecuteServo(servo8, 180)
            time.sleep(1)

      GPIO.output(bluePin, GPIO.LOW)
      GPIO.output(redPin, GPIO.LOW)

    elif getData == "enable bluetooth":
      # servoList = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
      servoList = [servo1, servo2]
      GPIO.output(redPin, GPIO.LOW)      
      GPIO.output(bluePin, GPIO.HIGH)
      PrintInfo()
      bServer = BluetoothServer(data_received)  #Received data from bluetooth
      
      while True:
          #Ask user for angle and turn servo to it
          try:            
            servoNo = getReceivedData()
            
            if servoNo == "0":
              GPIO.output(bluePin, GPIO.LOW)
              break
            elif(servoNo == "1"):
              DoMovement(servoList, 180)
              time.sleep(1.5)
              PrintInfo()
            elif(servoNo == "2"):
              DoMovement(servoList, 0)
              time.sleep(1.5)
              PrintInfo()
            elif(servoNo == "3"):
              DoMovement(servoList, 180)
              time.sleep(1.5)
              PrintInfo()
            elif(servoNo == "4"):
              DoMovement(servoList, 0)
              time.sleep(1.5)
              PrintInfo()
            elif(servoNo == "5"):
              for i in range(5):
                ExecuteServo(servo1, 180)
                ExecuteServo(servo2, 180)
                # ExecuteServo(servo3, 0)
                # ExecuteServo(servo4, 0)
                # ExecuteServo(servo5, 180)
                # ExecuteServo(servo6, 180)
                # ExecuteServo(servo7, 0)
                # ExecuteServo(servo8, 0)
                time.sleep(1)
                ExecuteServo(servo1, 0)
                ExecuteServo(servo2, 0)
                # ExecuteServo(servo3, 180)
                # ExecuteServo(servo4, 180)
                # ExecuteServo(servo5, 0)
                # ExecuteServo(servo6, 0)
                # ExecuteServo(servo7, 180)
                # ExecuteServo(servo8, 180)
                time.sleep(1)
              PrintInfo()
            elif(servoNo == "6"):
              for i in range(5):
                ExecuteServo(servo1, 0)
                ExecuteServo(servo2, 0)
                # ExecuteServo(servo3, 180)
                # ExecuteServo(servo4, 180)
                # ExecuteServo(servo5, 0)
                # ExecuteServo(servo6, 0)
                # ExecuteServo(servo7, 180)
                # ExecuteServo(servo8, 180)
                time.sleep(1)
                ExecuteServo(servo1, 180)
                ExecuteServo(servo2, 180)
                # ExecuteServo(servo3, 0)
                # ExecuteServo(servo4, 0)
                # ExecuteServo(servo5, 180)
                # ExecuteServo(servo6, 180)
                # ExecuteServo(servo7, 0)
                # ExecuteServo(servo8, 0)
                time.sleep(1)
              PrintInfo()
            
          except:
            pass
    elif getData == "close":
      break

finally:
  c.close()
  GPIO.cleanup()
  pause()

c.close()
GPIO.cleanup()
pause()