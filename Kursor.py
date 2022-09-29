import time
import pyautogui

while 1:
    x, y = pyautogui.position()
    xbin = bin(x)
    ybin = bin(y)
    with open('Logxy.txt', 'a') as f:
        f.write(str(xbin))
        f.write(str(ybin))
    time.sleep(0.3)
