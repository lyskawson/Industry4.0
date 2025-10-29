import time
import pigpio
import RPi.GPIO as GPIO

# --- Konfiguracja ---
# Piny GPIO (w trybie BCM) dla diod LED
LED_PINS = [17, 27, 22]  # Możesz zmienić na piny, których używasz
THRESHOLDS = [22.0, 24.0, 26.0]

# --- Inicjalizacja pigpio i SPI (zgodnie z obrazkiem/Listingiem 1) ---
pi = pigpio.pi()
if not pi.connected:
    print("Nie można połączyć się z demonem pigpio. Uruchom 'sudo pigpiod'.")
    exit(0)

# Używamy DOKŁADNYCH parametrów z dostarczonego przykładu
# kanał 1 (CE1), prędkość 1_000_000 bps (1MHz), flagi 0
sensor = pi.spi_open(1, 1000000, 0)

# --- Inicjalizacja RPi.GPIO dla diod LED ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Upewnij się, że wszystkie diody są zgaszone na starcie

def update_leds(temperature):
    """Zapala odpowiednią liczbę diod w zależności od temperatury."""
    num_leds_on = 0
    if temperature >= THRESHOLDS[0]:
        num_leds_on += 1
    if temperature >= THRESHOLDS[1]:
        num_leds_on += 1
    if temperature >= THRESHOLDS[2]:
        num_leds_on += 1
        
    print(f"Temperatura: {temperature:.2f}°C -> Zapalono {num_leds_on} z {len(LED_PINS)} diod.")
    
    # Pętla sterująca diodami
    for i, pin in enumerate(LED_PINS):
        if i < num_leds_on:
            GPIO.output(pin, GPIO.HIGH)  # Zapal diodę
        else:
            GPIO.output(pin, GPIO.LOW)   # Zgaś diodę

# --- Pętla główna ---
try:
    # Używamy pętli nieskończonej, aby program działał cały czas
    # Zamiast pętli działającej przez 600 sekund jak w przykładzie
    while True:
        # Odczyt danych z SPI - używamy oryginalnych nazw zmiennych 'c' i 'd'
        c, d = pi.spi_read(sensor, 2)
        
        if c == 2:  # Sprawdzamy, czy odczytano 2 bajty
            # Przetwarzanie danych (logika skopiowana 1:1 z Listingu 1)
            sign = (d[0] & 0x80) >> 7
            value = (((d[0] & 0x7f) << 8) | d[1]) >> 5
            temp = value * 0.125
            if sign == 1:
                temp = temp * -1
            
            # Wywołanie naszej dodanej funkcji do obsługi diod
            update_leds(temp)
        
        # Zgodnie z komentarzem w przykładzie, nie odczytujemy częściej niż 4 razy/sekundę
        time.sleep(0.5) # Zwiększyłem sleep, żeby konsola nie była zaśmiecana

except KeyboardInterrupt:
    print("\nProgram zakończony przez użytkownika.")

finally:
    pi.spi_close(sensor)
    pi.stop()
    GPIO.cleanup()
