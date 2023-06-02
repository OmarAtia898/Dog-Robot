import socket
import speech_recognition as sr
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

resultImage = "omer"
currentname = "unknown"
encodingsP = "encodings.pickle"


print("[INFO] loading encodings + face detector...")
data_cam = pickle.loads(open(encodingsP, "rb").read())

vs = VideoStream(0).start()
time.sleep(2.0)

fps = FPS().start()


r = sr.Recognizer()
mic = sr.Microphone()

s = socket.socket()

# Set the server's IP address and port
server_ip = '192.168.1.6'  # Replace with the actual server IP address
port = 12345

# Connect to the server
s.connect((server_ip, port))
print("Connected to the server")

# Send data to the server
while True:
    with mic as source:
        audio = r.listen(source, phrase_time_limit = 5)
    
    try:
        data = r.recognize_google(audio).lower()
        print(data)
        if data == "close":
            break
        elif data == "follow me":
            s.send(data.encode())
            for _ in range(15):
                frame = vs.read()
                frame = imutils.resize(frame, width=500)

                boxes = face_recognition.face_locations(frame)

                encodings = face_recognition.face_encodings(frame, boxes)
                names = []
                foundName = ""
                for encoding in encodings:
                    matches = face_recognition.compare_faces(data_cam["encodings"], encoding)

                    name = "Unknown"
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}			

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                        name = max(counts, key=counts.get)			

                        if currentname != name:
                            currentname = name
                print("Current name: ", currentname)
                if currentname == resultImage:
                    s.send(currentname.encode())
                time.sleep(1)




    except:
        print("unrecognized word")

# Close the connection
s.close()