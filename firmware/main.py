import board
import busio
import digitalio
import time

import adafruit_ssd1306

i2c = busio.I2C(scl=board.D7, sda=board.D6)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.show()

button = digitalio.DigitalInOut(board.D1)  # GPIO1 (GPI01)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

visual_modes = ["NameAndPronouns", "Time", "Weather"]
current_mode = 0
last_button_state = True

def update_display():
    display.fill(0)

    if visual_modes[current_mode] == "NameAndPronouns":
        display.text("Name: Lapis", 0, 0, 1)
        display.text("Pronouns: She/Her (Trans MtF)", 0, 10, 1)

    elif visual_modes[current_mode] == "Time":
        now = time.localtime()
        formatted = "{:02}:{:02}:{:02}".format(now.tm_hour, now.tm_min, now.tm_sec)
        display.text("Current Time:", 0, 0, 1)
        display.text(formatted, 0, 10, 1)

    elif visual_modes[current_mode] == "Weather":
	# too lazy to implement open-meteo api rn lol
        display.text("Weather:", 0, 0, 1)
        display.text("72F, Sunny", 0, 10, 1)

    display.show()

update_display()

while True:
    # Check for button press
    if not button.value and last_button_state:
        current_mode = (current_mode + 1) % len(visual_modes)
        update_display()
        last_button_state = False
    elif button.value and not last_button_state:
        last_button_state = True

    # Refresh time display once per loop
    if visual_modes[current_mode] == "Time":
        update_display()

    time.sleep(0.2)
