import board
import digitalio
import analogio
import usb_hid
import time
from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

button_pins = (board.GP12, board.GP13, board.GP14, board.GP15, board.GP22,)
gamepad_buttons = (1, 2, 3, 4, 9,) # Up to 16 buttons allowed I think
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

ax = analogio.AnalogIn(board.A0)
ay = analogio.AnalogIn(board.A1)

def debounce():
    time.sleep(0.01)

def calibrate(val):
    scaled_val = (val - 33000) / 127

    final_val = scaled_val * 0.49416342412

    return int(final_val)

while True:
    x_val = calibrate(ax.value)
    y_val = calibrate(ay.value)

    gp.move_joysticks(x=x_val, y=y_val)

    # print(f"Joystick X: {x_val:+4}, Y: {y_val:+4}")

    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
            # print(f"Button {gamepad_button_num}: Released")
        else:
            gp.press_buttons(gamepad_button_num)
            # print(f"Button {gamepad_button_num}: Pressed")

    debounce()
