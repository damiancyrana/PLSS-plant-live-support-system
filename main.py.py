from machine import Pin, ADC, I2C
import ssd1306
import time

# Ustawienia pinów do komunikacji I2C
I2C_SCL_PIN = 17  # Pin GP17 -> SCL wyświetlacza
I2C_SDA_PIN = 16  # Pin GP16 -> SDA wyświetlacza

# Inicjalizacja interfejsu I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

# Inicjalizacja wyświetlacza OLED
WIDTH = 128
HEIGHT = 32
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Definicje pinów
MOISTURE_SENSOR_PIN = 26  # GP26 - wejście ADC czujnika
SENSOR_POWER_PIN = 14     # GP14 - sterowanie zasilaniem czujnika
RELAY_PIN = 15            # GP15 - sterowanie przekaźnikiem

# Wartości ADC dla gleby suchej i mokrej
ADC_DRY = 26854
ADC_WET = 18290

# Interwał pomiaru w sekundach (np. co 3600 sekund = 1 godzina)
MEASUREMENT_INTERVAL = 10


class Plant:
    def __init__(self, name, ideal_moisture):
        self.name = name
        self.ideal_moisture = ideal_moisture


class MoistureSensor:
    def __init__(self, adc_pin, power_pin):
        self.adc = ADC(Pin(adc_pin))
        self.power = Pin(power_pin, Pin.OUT)
        self.power.value(0)

    def read_moisture(self):
        self.power.value(1)
        time.sleep(1)
        adc_value = self.adc.read_u16()
        self.power.value(0)
        return adc_value


class Relay:
    def __init__(self, pin):
        self.relay = Pin(pin, Pin.OUT)
        self.relay.value(0)

    def turn_on(self):
        self.relay.value(1)

    def turn_off(self):
        self.relay.value(0)


def normalize_moisture(adc_value):
    # Przeliczenie wartości ADC na procent wilgotności
    moisture_percent = ((adc_value - ADC_WET) / (ADC_DRY - ADC_WET)) * 100
    moisture_percent = max(0, min(100, moisture_percent))  # Ograniczenie do zakresu 0-100%
    return 100 - moisture_percent  # Odwrócenie, aby 100% było dla gleby mokrej

sensor = MoistureSensor(MOISTURE_SENSOR_PIN, SENSOR_POWER_PIN)
relay = Relay(RELAY_PIN)
basil = Plant("Bazylia", ideal_moisture=60)  # Idealna wilgotność 60%

while True:
    adc_value = sensor.read_moisture()
    moisture = normalize_moisture(adc_value)

    display.fill(0)
    display.text(f"Rosl.: {basil.name}", 0, 0)
    display.text(f"Wilg.: {moisture:.1f}%", 0, 10)

    if moisture < basil.ideal_moisture:
        relay.turn_on()
        display.text("Podlewanie...", 0, 20)
    else:
        relay.turn_off()
        display.text("Wilgotnosc OK", 0, 20)

    display.show()

    time.sleep(MEASUREMENT_INTERVAL)

