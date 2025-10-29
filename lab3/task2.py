import pygame
import ctypes
#from sensor import sensor_init, read_sensor
from time import sleep

def main():
    vl = ctypes.CDLL ( "/home/pi/krzysiuialek/vl6180_pi/libvl6180_pi.so" )

    vl.vl6180_initialise.argtypes = [ ctypes.c_int ]
    vl.vl6180_initialise.restype = ctypes.c_void_p
    vl.get_distance.argtypes = [ ctypes.c_void_p ]
    vl.get_distance.restype = ctypes.c_int
    vl.get_ambient_light.argtypes = [ ctypes.c_void_p , ctypes.c_int ]
    vl.get_ambient_light.restype = ctypes.c_float

    dev = vl . vl6180_initialise(0)
    GAIN = 6
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VL6180X Distance + light")
    font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            #distance, light = read_sensor(vl, dev)
            distance = vl.get_distance(dev)
            light = vl.get_ambient_light(dev, GAIN)
            print(f"Distance : {distance} mm , Light : {light:.2f}")
            sleep(0.5)
        except Exception:
            distance, light = 255, 0.0

        radius = max(10, 250 - int(distance))
        color = (max(0, 255 - int(distance)), 100, min(255, int(distance)))
        light_scaled = max(0, min(255, int(light)))
        light_color = (light_scaled, light_scaled, light_scaled)
        light_radius = max(10, int(light_scaled * 0.8))

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, color, (WIDTH // 3, HEIGHT // 2), radius)
        pygame.draw.circle(screen, light_color, (2 * WIDTH // 3, HEIGHT // 2), light_radius)

        text_d = font.render(f"{int(distance)} mm", True, (255, 255, 255))
        text_l = font.render(f"{light:.1f} lx", True, (255, 255, 255))
        screen.blit(text_d, (WIDTH // 3 - text_d.get_width() // 2, 50))
        screen.blit(text_l, (2 * WIDTH // 3 - text_l.get_width() // 2, 50))

        pygame.display.flip()
        clock.tick(10)
    pygame.quit()

if __name__ == "__main__":
    main()
