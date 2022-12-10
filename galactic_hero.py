# guitar hero for galactic unicorn

from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from galactic import GalacticUnicorn
from time import sleep

display = PicoGraphics(display=DISPLAY)
gu = GalacticUnicorn()
gu.set_brightness(0.25)


HEIGHT, WIDTH = display.get_bounds()

tune = ('00000',
        '00010',
        '00100',
        '10001')

GREEN = {'red':0,'green':255,'blue':0}
RED = {'red':255,'green':0,'blue':0}
YELLOW = {'red':255,'green':255,'blue':0}
CYAN = {'red':0,'green':255,'blue':255}
ORANGE = {'red':255,'green':128,'blue':0}
BLACK = {'red':0,'green':0,'blue':0}

def create_pen(display, color):
    return display.create_pen(color['red'],color['green'],color['blue'])

red = create_pen(display, RED)
green = create_pen(display, GREEN)
yellow = create_pen(display, YELLOW)
cyan = create_pen(display, CYAN)
orange = create_pen(display, ORANGE)
black = create_pen(display, BLACK)

fret_colours = {0:red, 1:green, 2:yellow, 3:cyan, 4:orange}

def set_row(fret,colour,row,col):
    print(f'fret: {fret}, colour:{colour}, row:{row}, col:{col}')
    if fret == '1':
        display.set_pen(colour)
    else:
        display.set_pen(colour)
    display.pixel(row,col)
    display.pixel(row,col+1)

def draw_notes(tune, y_pos):
    note_row = -1
    col = 0
    for note in tune:
        note_row += 1
        fret = list(note)
        fret_no = 0
        for frets in fret:
            colour = fret_colours[fret_no]
#             print(f'fret_no: {fret_no}')
            fret_no += 1
            set_row(fret=frets,colour=colour,row=note_row,col=y_pos+col)
            col += 2
#             print(f'row:{row}, col:{col}')
        
    gu.update(display)
    

row = 0
col = 0
pointer = 0
note_row = -1
count = 0
while True:
    draw_notes(tune,1)

    sleep(1)
    count += 1
    print(f'count: {count}')
    
#     for x in WIDTH:
#         for note in tune:
#             fret = list(note)
#             for frets in fret:
#                 colour = fret_colours[row]
#                 set_row(frets,colour,row,col)
#                 col += 2
#                 print(f'row:{row}, col:{col}')
#             col = 0
#             display.update()
#             sleep(1)
#         row += 1
#         print(fret)
    
