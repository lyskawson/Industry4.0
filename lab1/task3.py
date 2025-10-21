import RPi.GPIO as GPIO
import time
import random


# button_to_led_map = {
#     17: 19,
#     4: 18,
#     3: 13,
#     2: 12
# }

# button_pins = button_to_led_map.keys()
# led_pins = button_to_led_map.values()

led_pins = [19, 18, 13, 12]
button_pins= [17,4,3,2]

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

def signal_error():
    for pin in led_pins :
        GPIO.output(pin, 1)
    time.sleep(2) 

if __name__ == "__main__":
    setup_gpio()

    for i in range(0,3):
        try:
            
            correct_presses = 0
            reaction_times = []
            
            print("Starting game...")
            print("Get ready!!")

            time.sleep(3)

            while True:
                wait_time = random.uniform(1.0, 3.0)
                time.sleep(wait_time)

                choice_index = random.randint(0, 3)
                target_led = led_pins[choice_index]
                target_button = button_pins[choice_index]

                GPIO.output(target_led, 1)
                start_time = time.time()
                
                pressed_button_index = None
                while pressed_button_index is None:
                    for i, button_pin in enumerate(button_pins):
                        if GPIO.input(button_pin) == 0:
                            end_time = time.time()
                            pressed_button_index = i
                            break
                    time.sleep(0.01) 

                GPIO.output(target_led, 0)

                if pressed_button_index == choice_index:
                    reaction_time = end_time - start_time
                    reaction_times.append(reaction_time)
                    correct_presses += 1
                else:
                    signal_error()
                    for pin in led_pins :
                        GPIO.output(pin, 0)
                    break 
        
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        finally:
            if correct_presses > 0:
                best_time = min(reaction_times)
                avg_time = sum(reaction_times) / len(reaction_times)
                print(f"Corrects attempts: {correct_presses}")
                print(f"Best time: {best_time:.3f} s")
                print(f"Avg time: {avg_time:.3f} s")
        

            
    GPIO.cleanup()