import serial
import keyboard
import time
inkey=''
ser = serial.Serial('COM3', 9600, timeout = 0.01)
time.sleep(1)

while True:
    time.sleep(0.01)
    
    result = ser.read_all()
    print(result.decode())
    
    inkey = keyboard.read_key()
    
    if inkey != '':
        inkeys = bytes(inkey, 'utf-8')
        ser.write(inkeys)
        #print(inkeys)
        inkey =''
        
    
    
ser.close()
