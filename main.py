from chart import Chart
import pygame as pg
import random

pg.init()
screen = pg.display.set_mode((1280, 800))
clock = pg.time.Clock()
running = True
c1 = Chart((40, 50), (500, 300), "Voltage", screen)
c2 = Chart((40, 450), (500, 300), "Current", screen)
c3 = Chart((640, 50), (500, 300), "Power", screen)
c1.CHART_COLOR = (255, 0, 0)
c2.CHART_COLOR = (0, 255, 0)
c3.CHART_COLOR = (0, 0, 255)
prev = 50
prev2 = 50

# ser = serial.Serial(baudrate=9600, port="COM4")  # open serial port

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 800))
    c1.draw()
    c2.draw()
    c3.draw()
    pg.display.flip()
    clock.tick(60)
    prev += random.randint(-2, 2)
    prev2 += random.randint(-2, 2)
    c1.feed(prev)
    c2.feed(prev2)
    c3.feed(prev*prev2)

# ser.close()
pg.quit()
