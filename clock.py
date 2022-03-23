import math
import pygame as pg
import datetime
from pygame.locals import *


class Aplication():
    def __init__(self) -> None:
        self.width = 1280
        self.height = 768
        self.screen = pg.display.set_mode([self.width, self.height])
        print('Application has been Created')

    def clear(self):
        self.screen.fill((0, 0, 0))
        pg.display.flip()

    def loop(self):
        run = True
        pg.font.init()
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((80,80,80))
        self.screen.blit(background, (0, 0))

        clock = Clock(self.width/2, self.height/2)
        clock.init_pointers()

        while run:
            self.render(clock)
            clock.tick()

            for event in pg.event.get():
                if (event.type == MOUSEBUTTONDOWN):
                    print(pg.mouse.get_pos())

                if (event.type == KEYDOWN):
                    # print(event.__dict__)
                    if(event.key == 13 or event.key == 27):
                        print("Quiting")
                        run = False

                    # Increase
                    if(event.key == 1073741911):
                        print("Aumenta")

                    # Decrease
                    if(event.key == 1073741910):
                        print("Diminui")

    def draw_pointers(self, clock):
        for p in clock.pointers:
            if p:
                pg.draw.line(self.screen, p.color,
                             p.position, p.points_to, p.width)

        color = (0, 0, 166)
        pg.draw.circle(self.screen, color, clock.position, 8)
        color = (0, 0, 255)
        pg.draw.circle(self.screen, color, clock.position, 4)
        color = (96, 96, 255)
        pg.draw.circle(self.screen, color, clock.position, 2)

    def draw_dashes(self, clock):
        dashes = 12
        color = (238, 173, 45)
        angle = 0
        angle_rate = 360 / dashes  # 30
        clock_center = (self.width / 2, self.height / 2)
        distance = 260

        for i in range(dashes):
            angle += angle_rate % 360  # + 30, limit 330
            rad = math.radians(angle-90)
            numbers_angle_rate = 360/len(clock.numbers)  # 90

            if (angle not in [90, 180, 270, 360]): #Don't draw in the numbers's space
                x = int(clock_center[0] + math.cos(rad) * distance)
                y = int(clock_center[1] + math.sin(rad) * distance)

                pg.draw.circle(self.screen, color, (x, y), 4)

    def draw_numbers(self, clock):
        numbers = clock.numbers
        # Instance of Font
        font = pg.font.SysFont('Arial', 50)
        clock_center = (self.width / 2, self.height / 2)
        distance = 260
        color = (238, 173, 45)

        angle = 0
        # Finds the angle rate
        angle_rate = 360 / len(numbers)  # 90

        for n in numbers:
            angle += angle_rate % 360
            rad = math.radians(angle-90)
            img_center = [i / 2 for i in pg.font.Font.size(font, n)]
            x = int(clock_center[0] + math.cos(rad) * distance)
            y = int(clock_center[1] + math.sin(rad) * distance)
            x = x - img_center[0]
            y = y - img_center[1]

            self.screen.blit(font.render(n, True, color), (x, y))

    def render(self, clock):
        pg.draw.circle(self.screen, clock.color, clock.position, clock.size)
        self.draw_numbers(clock)
        self.draw_dashes(clock)
        self.draw_pointers(clock)

        pg.display.flip()


class Clock():
    def __init__(self, x, y):
        self.position = (x, y)
        self.size = 300
        self.numbers = ['3', '6', '9', '12']
        self.color = (211, 211, 211)
        self.pg_clock = pg.time.Clock()
        self.seconds_pointer = Pointer(x, y, 'sec', self.size*0.9, True, 2)
        self.minutes_pointer = Pointer(x, y, 'min', self.size*0.7, False, 5)
        self.hours_pointer = Pointer(x, y, 'hour', self.size*0.5, False, 5)
        self.pointers = [self.seconds_pointer,
                         self.minutes_pointer, self.hours_pointer]

    def init_pointers(self):
        now = datetime.datetime.now()
        hh = now.strftime('%H')
        mm = now.strftime('%M')
        ss = now.strftime('%S')
        ss = 30

        for p in self.pointers:
            if p:
                # Sets init position for seconds pointer
                if (p.label == 'sec'):
                    p.angle = int(ss) * self.get_angle_rate(p)
                # Sets init position for minutes pointer
                elif (p.label == 'min'):
                    p.angle = int(mm) * self.get_angle_rate(p)
                # Sets init position for hours pointer
                else:
                    p.angle = int(hh) * self.get_angle_rate(p) * 60
                    # Sums the minutes variation to the minutes pointer
                    minutes_variation = (
                        int(mm) * self.get_angle_rate(self.hours_pointer))
                    p.angle = p.angle + minutes_variation

                p.rad = math.radians(p.angle-90)

                # Calculates the point considering the center
                x = int(p.position[0] + math.cos(p.rad) * p.size)
                y = int(p.position[1] + math.sin(p.rad) * p.size)

                # The end point of each pointer
                p.points_to = (x, y)

    def tick(self):
        self.move_pointers()
        pg.time.delay(1000)

    def move_pointers(self):
        for p in self.pointers:
            if p and p.update:
                p.angle = (p.angle + self.get_angle_rate(p)) % 360
                p.rad = math.radians(p.angle-90)

                x = int(p.position[0] + math.cos(p.rad) * p.size)
                y = int(p.position[1] + math.sin(p.rad) * p.size)

                p.points_to = (x, y)

                self.setUpdate(p)

    def setUpdate(self, p):
        if ((p.label == 'sec' and p.angle == 0) or (p.label == 'min' and self.minutes_pointer.update == True)):
            self.minutes_pointer.update = True
            self.hours_pointer.update = True
        else:
            self.minutes_pointer.update = False
            self.hours_pointer.update = False

    def get_angle_rate(self, p) -> int:
        rates = {'sec': 6, 'min': 6, 'hour': 0.5}
        return rates[p.label]


class Pointer():
    def __init__(self, x, y, label, size, update, width):
        self.position = (x, y)
        self.color = (0, 0, 255)
        self.width = width
        self.points_to = (640, 84)
        self.label = label
        self.size = size
        self.rad = 0
        self.angle = 0
        self.value = 0
        self.update = update

    def updateValue(self):
        self.value += 1
        self.value = self.value % 60


if __name__ == "__main__":
    ap = Aplication()

    ap.loop()
