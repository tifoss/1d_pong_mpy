from microbit import *
import neopixel

np = neopixel.NeoPixel(pin0, 60)
np.fill((0,0,100))
for i in range(0,5):
    np[i] = (0,255,0)
for i in range(55,60):
    np[i] = (0,255,0)

i = 0
step = 1
last = np[0]
while True:
    np[i] = (255,255,255)
    
    pin8.set_pull(pin8.PULL_UP)
    if not pin8.read_digital():
        pin1.write_analog(0)
    else:
        if i > 30:
            pin1.write_analog(1023)
        else:
            pin1.write_analog(511)

    pin16.set_pull(pin16.PULL_UP)
    if not pin16.read_digital():
        pin2.write_analog(0)
    else:
        if i > 30:
            pin2.write_analog(1023)
        else:
            pin2.write_analog(511)

    np.write()
    np.show()
    
    sleep(10)
    
    np[i] = last
    i = i + step
    if i == 59:
        step = -1
    elif i == 0:
        step = 1
    last = np[i]
