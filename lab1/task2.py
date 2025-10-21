import RPi.GPIO as GPIO
import time

button_to_led_map = {
    17: 19,
    4: 18,
    3: 13,
    2: 12
}

button_pins = button_to_led_map.values()
led_pins = button_to_led_map.keys()

led_states = {} 
for pin in led_pins:
    led_states[pin] = 0

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for led_pin in led_pins:
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.output(led_pin, 0) 

    for button_pin in button_pins:
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == "__main__":
    try:
        setup_gpio()
        should_exit = False
        
        while not should_exit:
            for button_pin, led_pin in button_to_led_map.items():
                
                if GPIO.input(button_pin) == 0: 
                    current_state = led_states[led_pin]
                    new_state = 1 if current_state == 0 else 0
                    
                    GPIO.output(led_pin, new_state)
                    led_states[led_pin] = new_state
                    
                    if new_state == 0:
                        should_exit = True 
                    

                    time.sleep(0.15)
                    
                    if should_exit == True:
                        break 
            
            time.sleep(0.15) 

    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        GPIO.cleanup()