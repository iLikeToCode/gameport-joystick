import time
import threading
import serial
import vgamepad
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

ser = None
keep_running = True
gamepad = vgamepad.VX360Gamepad()

def map_analog(value, invert=False):
    # Clamp value between 75 and 1023
    value = max(75, min(1023, value))
    if invert:
        value = 1023 - (value - 75)  # Invert around the clamped range

    # Map [75, 1023] -> [-32768, 32767]
    return int((value - 75) / (1023 - 75) * 65535 - 32768)

def read_serial():
    global ser
    while keep_running:
        try:
            if ser is None or not ser.is_open:
                try:
                    ser = serial.Serial('COM4', 9600, timeout=1)
                except:
                    time.sleep(2)
                    continue

            line = ser.readline().decode('utf-8').strip()
            if not line.startswith("X:"):
                continue

            parts = line.split()
            x = int(parts[1])
            y = int(parts[3])
            btn1 = parts[5] == "PRESSED"
            btn2 = parts[7] == "PRESSED"

            x_mapped = map_analog(x, invert=True)
            y_mapped = map_analog(y, invert=False)

            gamepad.left_joystick(x_value=x_mapped, y_value=y_mapped)

            if btn1:
                gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
            else:
                gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)

            if btn2:
                gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
            else:
                gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)

            gamepad.update()

        except:
            time.sleep(1)
        time.sleep(0.01)

def create_icon():
    img = Image.new('RGB', (64, 64), 'black')
    draw = ImageDraw.Draw(img)
    draw.rectangle((16, 16, 48, 48), fill='white')
    return img

def on_exit(icon, item):
    global keep_running
    keep_running = False
    if ser and ser.is_open:
        ser.close()
    icon.stop()

def main():
    icon = Icon("arduino_gamepad", icon=create_icon(), menu=Menu(MenuItem("Exit", on_exit)))
    threading.Thread(target=read_serial, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()

