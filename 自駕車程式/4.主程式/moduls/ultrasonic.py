# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class SuperSonic:
    

    def __init__(self,trigger_pin = 17,echo_pin = 27):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
    
        GPIO.setwarnings(0)
        GPIO.setmode(GPIO.BCM)
    
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    
    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.001)
        GPIO.output(self.trigger_pin, False)

    def wait_for_echo(self,value, timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count > 0:
            count = count - 1

    def get_distance(self):
        self.send_trigger_pulse()
        self.wait_for_echo(True, 5000)
        start = time.time()
        self.wait_for_echo(False, 5000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len * 340 *100 /2
        # distance_in = distance_cm / 2.5   #換算成inch
        return distance_cm 



