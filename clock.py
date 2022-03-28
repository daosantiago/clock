import math
import pygame as pg
import datetime
from settings import CLOCK_SETTINGS, APP_SETTINGS
from pygame.locals import *

COLORS = {
    'bg_clock': (211, 211, 211),
    'dash': (238, 173, 45),
    'center': [(41, 107, 155), (70, 130, 180), (97, 154, 205)],
    'number': (237, 145, 33),
    'pointer': (41, 107, 155),
    'bg': (80,80,80)
}
class Application():
    def __init__(self) -> None:
        self.width = APP_SETTINGS['width']
        self.height = APP_SETTINGS['height']
        self.screen = pg.display.set_mode([self.width, self.height])
        self.center = (self.width / 2, self.height / 2)
        pg.display.set_caption('My Clock')
        
        print('Application has been Created')

    def clear(self):
        self.screen.fill((0, 0, 0))
        pg.display.flip()

    def loop(self):
        run = True
        pg.font.init()
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(COLORS['bg'])
        self.screen.blit(background, (0, 0))

        clock = Clock(self.center)
        clock.init()

        ticker = pg.time.Clock()

        while run:
            self.render(clock)
            clock.move_pointers()
            ticker.tick(1)

            for event in pg.event.get():
                if (event.type == MOUSEBUTTONDOWN):
                    print(pg.mouse.get_pos())

                if (event.type == pg.QUIT):
                    run = False

                if (event.type == KEYDOWN):
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
        """Draws the pointers"""
        for p in clock.pointers:
            if p:
                pg.draw.line(self.screen, p.color,
                             p.position, p.points_to, p.width)

        #Draws three points in the middle to simulate 3D
        color = COLORS['center'][0]
        pg.draw.circle(self.screen, color, clock.position, 8)
        color = COLORS['center'][1]
        pg.draw.circle(self.screen, color, clock.position, 5)
        color = COLORS['center'][2]
        pg.draw.circle(self.screen, color, clock.position, 2)

    def draw_dashes(self, clock):
        """Draws the dots where there's no numbers.
        If there should be a number there, draws a larger dot"""
        dashes = 60
        color = COLORS['dash']
        angle = 0
        angle_rate = 360 / dashes  # 30
        distance = 280

        for i in range(dashes):
            angle += angle_rate % 360  # + 30, limit 330
            rad = math.radians(angle-90)
            numbers_angle_rate = 360/len(clock.numbers)  # 90

            #Big dots in places where there should be a number
            size = 5
            #Small dots where there's a number
            if ((angle % 30 != 0) or (angle % numbers_angle_rate == 0)):
                size = 2            

            x, y = self.set_position(rad, distance)

            pg.draw.circle(self.screen, color, (x, y), size)

    def draw_numbers(self, clock):
        numbers = clock.numbers
        # Instance of Font
        font = pg.font.SysFont('Arial', 50)        
        distance = 255
        color = COLORS['number']

        angle = 0
        # Finds the angle rate
        angle_rate = 360 / len(numbers)  # 90

        for n in numbers:
            angle += angle_rate % 360
            rad = math.radians(angle-90)
            #Finds the center of the images created to draw the number
            img_center = [i / 2 for i in pg.font.Font.size(font, n)]
            
            x, y = self.set_position(rad, distance)

            x = x - img_center[0]
            y = y - img_center[1]

            self.screen.blit(font.render(n, True, color), (x, y))

    def set_position(self, rad, distance):
        x = int(self.center[0] + math.cos(rad) * distance)
        y = int(self.center[1] + math.sin(rad) * distance)

        return x, y
        
    def render(self, clock):
        pg.draw.circle(self.screen, clock.color, clock.position, clock.size)
        self.draw_numbers(clock)
        self.draw_dashes(clock)
        self.draw_pointers(clock)

        pg.display.flip()


class Clock():
    def __init__(self, center):
        self.position = (center[0], center[1])
        self.size = APP_SETTINGS['height'] * 0.40
        self.numbers = CLOCK_SETTINGS['numbers']
        self.color = COLORS['bg_clock']
        self.pg_clock = pg.time.Clock()
        self.seconds_pointer = Pointer(center[0], center[1], 'sec', self.size*0.9, True, 2)
        self.minutes_pointer = Pointer(center[0], center[1], 'min', self.size*0.7, False, 5)
        self.hours_pointer = Pointer(center[0], center[1], 'hour', self.size*0.5, False, 5)
        self.pointers = [self.seconds_pointer,
                         self.minutes_pointer, self.hours_pointer]

    def init(self):
      self.init_pointers()

    def init_pointers(self):
        """Initialize the pointers according to the CPU time"""
        now = datetime.datetime.now()
        hh = now.strftime('%H')
        mm = now.strftime('%M')
        ss = now.strftime('%S')
        
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
        """Controls if the pointer should be updated"""
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
        self.color = COLORS['pointer']
        self.width = width
        self.points_to = None
        self.label = label
        self.size = size
        self.rad = 0
        self.angle = 0
        self.update = update


if __name__ == "__main__":
    ap = Application()

    ap.loop()