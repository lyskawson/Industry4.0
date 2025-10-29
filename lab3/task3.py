import pygame
import ctypes
from random import randint
import RPi.GPIO as GPIO
from time import sleep

def main():
    
    vl = ctypes.CDLL("/home/pi/krzysiuialek/vl6180_pi/libvl6180_pi.so")
    vl.vl6180_initialise.argtypes = [ctypes.c_int]
    vl.vl6180_initialise.restype = ctypes.c_void_p
    vl.get_distance.argtypes = [ctypes.c_void_p]
    vl.get_distance.restype = ctypes.c_int
    vl.get_ambient_light.argtypes = [ctypes.c_void_p, ctypes.c_int]
    vl.get_ambient_light.restype = ctypes.c_float

    dev = vl.vl6180_initialise(0)
    GAIN = 6

  
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    BUTTON_PIN = 17  
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  
    pygame.init()
    W, H = 600, 400
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    ground = H - 60
    x, y = 80, ground
    vy = 0
    g = 1
    jump = -14
    cactus_x = W
    cactus_w, cactus_h = 30, 50
    speed = 6
    score = 0
    running = True
    game_over = False

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

       
        if GPIO.input(BUTTON_PIN) == 0 and not game_over:
            if y >= ground:
                vy = jump
                sleep(0.2)

   
        try:
            light = vl.get_ambient_light(dev, GAIN)
        except:
            light = 100.0

        bg = max(0, min(255, int(light)))
        screen.fill((bg//4, bg//4, bg//4))

        vy += g
        y += vy
        if y > ground:
            y, vy = ground, 0

        if not game_over:
            cactus_x -= speed
            if cactus_x + cactus_w < 0:
                cactus_x = W + randint(100, 200)
                speed = min(14, speed + 0.3)
                score += 1

        
        dino = pygame.Rect(x, y - 40, 40, 40)
        cactus = pygame.Rect(cactus_x, ground - cactus_h, cactus_w, cactus_h)

        pygame.draw.rect(screen, (240, 240, 240), dino, border_radius=6)
        pygame.draw.rect(screen, (200, 80, 60), cactus, border_radius=4)
        pygame.draw.line(screen, (180, 180, 180), (0, ground+40), (W, ground+40), 3)

    
        if dino.colliderect(cactus) and not game_over:
            game_over = True
            pygame.time.delay(500)

        
        if game_over:
            txt_game_over = font.render("GAME OVER! Press button to restart", True, (255, 80, 80))
            screen.blit(txt_game_over, (50, 150))
            if GPIO.input(BUTTON_PIN) == 0:
                
                y, vy = ground, 0
                cactus_x = W
                score = 0
                speed = 6
                game_over = False
                sleep(0.5)

        
        txt = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(txt, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
