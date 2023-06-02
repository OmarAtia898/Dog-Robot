import socket
import speech_recognition as sr


for device_index in sr.Microphone.list_working_microphones():
    mic = sr.Microphone(device_index=device_index)
    print(device_index)
else:
    print("No working microphones found!")
