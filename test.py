from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from time import sleep
from galactic import GalacticUnicorn

gu = GalacticUnicorn()
display = PicoGraphics(display=DISPLAY)
gu.set_brightness(0.25)

WIDTH, HEIGHT = display.get_bounds()

# RED = display.create_pen(255,0,0)
# BLACK = display.create_pen(0,0,0)
GREEN = {'red':0,'green':255,'blue':0}
RED = {'red':255,'green':0,'blue':0}
YELLOW = {'red':255,'green':255,'blue':0}
CYAN = {'red':0,'green':255,'blue':255}
ORANGE = {'red':255,'green':128,'blue':0}
BLACK = {'red':0,'green':0,'blue':0}
WHITE = {'red':255,'green':255, 'blue':255}

def create_pen(display, color):
    return display.create_pen(color['red'],color['green'],color['blue'])

red = create_pen(display, RED)
green = create_pen(display, GREEN)
yellow = create_pen(display, YELLOW)
cyan = create_pen(display, CYAN)
orange = create_pen(display, ORANGE)
black = create_pen(display, BLACK)
white = create_pen(display, WHITE)

fret_colours = {0:red, 1:green, 2:yellow, 3:cyan, 4:orange}

# Set the game button states
fret_a = False
fret_b = False
fret_c = False
fret_d = False
fret_e = False
winning = True

tune = ('01110',
        '10001',
        '10001',
        '11011',
        '01110',
        '00001',
        '00010',
        '00100',
        '01000',
        '10000',
        '01000',
        '00100',
        '00010',
        '00001',
        '00010',
        '00100',
        '01000',
        '10000',
        '01000',
        '00100',
        '00010',
        '00001',
        '00000',
        '00001',
        '00000',
        '00001',
        '00000',
        '00001',
        '00000',
        '00001',
        '00000'
        )

def transpose(bitmap):
    """ Transpose a bitmap """
    transposed_bitmap = [''.join([string[i] for string in bitmap]) for i in range(len(bitmap[0]))]
    return transposed_bitmap

def display_tune(bitmap, x:int, y:int):
    global fret_a, fret_b, fret_c, fret_d, fret_e
    row_offset = 0
    col_offset = 0
    fret_a = False
    fret_b = False
    fret_c = False
    fret_d = False
    fret_e = False
    for row in bitmap:
        row_offset = 0
        fret_no = 0
        for pixel in row:
            # check if row is on screen
            if len(row)+row_offset < WIDTH:
                
                if len(bitmap)+(col_offset//2) < HEIGHT:
                    if pixel == '1':
                        colour = fret_colours[col_offset//2]
                        display.set_pen(colour)
                    else:
                        display.set_pen(black)
                    display.pixel(x+row_offset, y+col_offset)
                    display.pixel(x+row_offset, y+col_offset+1)
                    
                    # set the game state
                    if x+row_offset >= 51:
                        if y+col_offset == 0: fret_e = True
                        if y+col_offset == 2: fret_d = True
                        if y+col_offset == 4: fret_c = True
                        if y+col_offset == 6: fret_b = True
                        if y+col_offset == 8: fret_a = True
                           
                else:
                    offset = len(bitmap)+col_offset
            fret_no += 1
            row_offset += 2 

        col_offset += 2
        
def display_board():
    """ Display the gameboard"""
    display.set_pen(white)
    display.line(50,0,50,11)
    display.update()
        
def check_buttons():
    fail = False
    button_a = GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN
    button_b = GalacticUnicorn.SWITCH_BRIGHTNESS_UP
    button_c = GalacticUnicorn.SWITCH_SLEEP
    button_d = GalacticUnicorn.SWITCH_VOLUME_DOWN
    button_e = GalacticUnicorn.SWITCH_VOLUME_UP

#     print(f'checking button_a')
    if gu.is_pressed(button_a) and fret_a:
        fail = False
    else: fail = True
    if gu.is_pressed(button_b) and fret_b:
        fail = False
    else: fail = True
    if gu.is_pressed(button_c) and fret_c:
        fail = False
    else: fail = True
    if gu.is_pressed(button_d) and fret_d:
        fail = False
    else: fail = True
    if gu.is_pressed(button_e) and fret_e:
        fail = False
    else: fail = True
#     print(f'fail: {fail}')
    return fail

def check_missed():
    if fret_a or fret_b or fret_c or fret_d or fret_e:
        display.set_pen(red)
        display.rectangle(50,0,1,11)
#         display.update()
        return True
    else:
        return False
    
new_tune = transpose(tune)
x_reset = -len(new_tune[0]*2)
x = x_reset
y = 0

winning = True
while True and winning:
    display.set_pen(black)
    display.clear()
    display_board()
    display_tune(new_tune,x,y)
    check_missed()
    winning = check_buttons()
#     print(f'winning: {winning}')
    
#     print(f'x is {x}')
    x = x + 1
    gu.update(display)
    sleep(0.1)
    offset = x - len(new_tune[0])
#     print(f'offset is {offset}, WIDTH is {WIDTH}')
    if offset > WIDTH-4:
        x = x_reset
    
print("you lost")