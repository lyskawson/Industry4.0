import RPi.GPIO as GPIO
import time

led_pins = [19, 18, 13, 12]

def setup_gpio():
    GPIO.setwarnings(False)  
    GPIO.setmode(GPIO.BCM)   
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)  
        GPIO.output(pin, GPIO.LOW) 

def led_cycle():
    for pin in led_pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pin, GPIO.LOW)
    
    for pin in led_pins:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)
    

if __name__ == "__main__":
    try:
        setup_gpio()
        
        for i in range(3):
            led_cycle()
            time.sleep(1) 

    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        GPIO.cleanup() 