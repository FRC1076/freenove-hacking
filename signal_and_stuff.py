import time
from Led import *
import Motor
from threading import Thread, enumerate


def blink_left(led):
    led.ledIndex(0xFF, 0, 0, 0)
    while True:
        led.ledIndex(0x24, 255, 255, 0)
        time.sleep(0.5)
        led.ledIndex(0xFF, 0, 0, 0)
        

def blink_right(led):
    led.ledIndex(0xFF, 0, 0, 0)
    while True:
        led.ledIndex(0x42, 255, 255, 0)
        time.sleep(0.5)
        led.ledIndex(0xFF, 0, 0, 0)
        

class Signaller():
    
    def __init__(self, led):
        self.led = led
        self.current_thread = None
        self.current_thread_running = False
        
    def forward(self):
        self.current_thread_running = False
        led.ledIndex(0xFF, 0, 0, 0)
        led.ledIndex(0x06, 255, 0, 0)
        led.ledIndex(0x60, 255, 255, 255)
    
    def backward(self):
        self.current_thread_running = False
        led.ledIndex(0xFF, 0, 0, 0)
        led.ledIndex(0x60, 255, 0, 0)
        led.ledIndex(0x06, 255, 255, 255)
        
    def stop(self):
        self.current_thread_running = False
        led.ledIndex(0xFF, 0, 0, 0)
        led.ledIndex(0xFF, 0, 255, 0)
        
    def left(self):
        led.ledIndex(0xFF, 0, 0, 0)
        while self.current_thread_running:
            led.ledIndex(0x24, 255, 255, 0)
            time.sleep(1)
            led.ledIndex(0xFF, 0, 0, 0)
            time.sleep(1)
        
    def left_blink(self):
        self.current_thread_running = False
        self.current_thread = Thread(target=self.left)
        self.current_thread_running = True
        self.current_thread.start()
        
    def right(self):
        self.current_thread_running = False
        led.ledIndex(0xFF, 0, 0, 0)
        led.ledIndex(0x42, 255, 255, 0)
        
        
class DriveTrain():
    def __init__(self, motor):
        self.motor = motor
        
    def forward(self):
        self.motor.setMotorModel(-2000,-2000,-2000,-2000)
        
    def backward(self):
        self.motor.setMotorModel(2000,2000,2000,2000)
        
    def stop(self):
        self.motor.setMotorModel(0,0,0,0)
        
    def left(self):
        self.motor.setMotorModel(0, 0, -2000, -2000)
        
    def right(self):
        self.motor.setMotorModel(-2000, -2000, 0, 0)
        

class SignalDriveTrain():
    def __init__(self, led, motor):
        self.signaller = Signaller(led)
        self.drive_train = DriveTrain(motor)
        
    def forward(self):
        self.drive_train.forward()
        self.signaller.forward()
    
    def backward(self):
        self.drive_train.backward()
        self.signaller.backward()
    
    def stop(self):
        self.drive_train.stop()
        self.signaller.stop()
    
    def left(self):
        self.drive_train.left()
        self.signaller.left()
    
    def left_blink(self):
        self.drive_train.left()
        self.signaller.left_blink()
        
    def right(self):
        self.drive_train.right()
        self.signaller.right()
        
        
def test_Led():
    try:
        for i in range(0,8):
            select = 1 << i
            print("Lighting index",i)
            led.ledIndex(select, 100, 0, 100)
            time.sleep(3)
            

        led.ledIndex(0x01,255,0,0)     
        led.ledIndex(0x02,255,125,0)    #orange
        led.ledIndex(0x04,255,255,0)    #yellow
        led.ledIndex(0x08,0,255,0)      #green
        led.ledIndex(0x10,0,255,255)    #cyan-blue
        led.ledIndex(0x20,0,0,255)      #blue
        led.ledIndex(0x40,128,0,128)    #purple
        led.ledIndex(0x80,255,255,255)  #white'''
        print ("The LED has been lit, the color is red orange yellow green cyan-blue blue white")
        time.sleep(3)               #wait 3s
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        print ("\nEnd of program")
    except KeyboardInterrupt:
        led.colorWipe(led.strip, Color(0,0,0))  #turn off the light
        print ("\nEnd of program")

        
if __name__ == "__main__":
    led = Led()
    PWM=Motor.Motor()           
    #test_Led()
    #led.theaterChaseRainbow(led.strip)
    """
    signaller.forward()
    time.sleep(5)
    signaller.backward()
    """
    drive_train = SignalDriveTrain(led, PWM)
    for _ in range(5):
        drive_train.forward()
        time.sleep(3)
        drive_train.backward()
        time.sleep(4)
        drive_train.left_blink()
        time.sleep(3)
        drive_train.right()
        time.sleep(3)
    drive_train.stop()
    
