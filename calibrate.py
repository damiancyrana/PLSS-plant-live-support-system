from machine import Pin, I2C, ADC
import ssd1306
import time

# Ustawienia pinów do komunikacji I2C
I2C_SCL_PIN = 17  # Pin GP17 -> SCL wyświetlacza
I2C_SDA_PIN = 16  # Pin GP16 -> SDA wyświetlacza

# Ustawienia pinu dla czujnika wilgotności gleby
SOIL_MOISTURE_PIN = 26  # Pin GP26 (ADC0)

# Inicjalizacja interfejsu I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

# Inicjalizacja wyświetlacza OLED
WIDTH = 128
HEIGHT = 32

display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
soil_moisture = ADC(Pin(SOIL_MOISTURE_PIN))

adc_values = []
display.fill(0)
display.text('Trwa pomiar...', 0, 0)
display.show()

for i in range(30): # Pomiary przez 30 sekund
    # Odczyt surowej wartości z ADC (0 - 65535)
    adc_value = soil_moisture.read_u16()
    adc_values.append(adc_value)
    display.fill(0) 
    display.text('ADC Value:', 0, 0)
    display.text(str(adc_value), 0, 10)
    display.show()
    time.sleep(1)  # Odczekaj 1 sekundę przed kolejnym pomiarem

average_adc = sum(adc_values) / len(adc_values)
display.fill(0)
display.text('Srednia wartosc ADC:', 0, 0)
display.text(str(int(average_adc)), 0, 10)
display.show()


while True:
    time.sleep(1)

