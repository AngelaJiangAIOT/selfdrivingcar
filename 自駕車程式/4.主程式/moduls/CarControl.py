import RPi.GPIO as GPIO
# import pigpio

class CarControl:
    
    def __init__(self,M_A_F = 18,M_A_B = 23,M_B_F = 24,M_B_B = 25,ENA = 12,ENB = 13):
    
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.ENA = ENA
        self.ENB = ENB
        self.M_A_F = M_A_F
        self.M_A_B = M_A_B
        self.M_B_F = M_B_F
        self.M_B_B = M_B_B
#         self.PWM_FREQ = 800
        GPIO.setup(self.M_A_F,GPIO.OUT)
        GPIO.setup(self.M_A_B,GPIO.OUT)
        GPIO.setup(self.M_B_F,GPIO.OUT)
        GPIO.setup(self.M_B_B,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        
        self.Motor_A =GPIO.PWM(self.ENA,100)
        self.Motor_A.start(0)
        self.Motor_B =GPIO.PWM(self.ENB,100)
        self.Motor_B.start(0)
#         self.pi = pigpio.pi() # https://reurl.cc/vDGNDN 
        
    def Forward(self,Motor_A,Motor_B):
       
        self.Motor_A.ChangeDutyCycle(Motor_A)
#         self.pi.hardware_PWM(self.ENA, self.PWM_FREQ, Motor_A)
        GPIO.output(self.M_A_F,1)
        GPIO.output(self.M_A_B,0)
        
#         self.pi.hardware_PWM(self.ENB, self.PWM_FREQ, Motor_B)
        self.Motor_B.ChangeDutyCycle(Motor_B)
        GPIO.output(self.M_B_F,1)
        GPIO.output(self.M_B_B,0)

        
        
    def Reverse(self):
        self.Motor_A.ChangeDutyCycle(100)
        self.Motor_B.ChangeDutyCycle(100)
        GPIO.output(self.M_A_F,0)
        GPIO.output(self.M_A_B,1)
        GPIO.output(self.M_B_F,0)
        GPIO.output(self.M_B_B,1)
        
        
    def turnRight(self):
        self.Motor_A.ChangeDutyCycle(100)
        self.Motor_B.ChangeDutyCycle(100)
        GPIO.output(self.M_A_F,0)
        GPIO.output(self.M_A_B,1)
        GPIO.output(self.M_B_F,1)
        GPIO.output(self.M_B_B,0)

        
    def turnLeft(self):
        self.Motor_A.ChangeDutyCycle(100)
        self.Motor_B.ChangeDutyCycle(100)
        GPIO.output(self.M_A_F,1)
        GPIO.output(self.M_A_B,0)
        GPIO.output(self.M_B_F,0)
        GPIO.output(self.M_B_B,1)
 
        
    def stop(self):
        self.Motor_A.ChangeDutyCycle(0)
        self.Motor_B.ChangeDutyCycle(0)
        GPIO.output(self.M_A_F,0)
        GPIO.output(self.M_A_B,0)
        GPIO.output(self.M_B_F,0)
        GPIO.output(self.M_B_B,0)
        
    
    def __del__(self):
        print("Car Destroyed!! ")
        