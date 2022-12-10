# Galactic Hero - A game for the Pimoroni Pico Display
# Kevin McAleer
# December 2022

from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from time import sleep
from galactic import GalacticUnicorn

# Set up the display
gu = GalacticUnicorn()
display = PicoGraphics(display=DISPLAY)
gu.set_brightness(0.25)
WIDTH, HEIGHT = display.get_bounds()

# Set up the colours
GREEN = {'red':0,'green':255,'blue':0}
RED = {'red':255,'green':0,'blue':0}
YELLOW = {'red':255,'green':255,'blue':0}
CYAN = {'red':0,'green':255,'blue':255}
ORANGE = {'red':255,'green':128,'blue':0}
BLACK = {'red':0,'green':0,'blue':0}
WHITE = {'red':255,'green':255, 'blue':255}

def create_pen(display, color):
    """ Create a pen from a colour dictionary """
    return display.create_pen(color['red'],color['green'],color['blue'])

# Create the pens
red = create_pen(display, RED)
green = create_pen(display, GREEN)
yellow = create_pen(display, YELLOW)
cyan = create_pen(display, CYAN)
orange = create_pen(display, ORANGE)
black = create_pen(display, BLACK)
white = create_pen(display, WHITE)

# Set the fret colours
fret_colours = {0:red, 1:green, 2:yellow, 3:cyan, 4:orange}

# Set the game button states
fret_a = False
fret_b = False
fret_c = False
fret_d = False
fret_e = False
winning = True

# Create the tune pattern - moved to a file
from tune01 import tune

def transpose(bitmap):
    """ Transpose a bitmap (This is because the Galactic Unicorn is rotated 90 degrees) """
    transposed_bitmap = [''.join([string[i] for string in bitmap]) for i in range(len(bitmap[0]))]
    return transposed_bitmap

def display_tune(bitmap, x:int, y:int):
    """ Display a tune on the screen at x,y coordinates """
    global fret_a, fret_b, fret_c, fret_d, fret_e
    row_offset = 0
    col_offset = 0
    fret_a = False
    fret_b = False
    fret_c = False
    fret_d = False
    fret_e = False
    # Loop through each row of the bitmap
    for row in bitmap:
        row_offset = 0
        fret_no = 0
        # Loop through each pixel in the row
        for pixel in row:
            # check if row is on screen, within the bounds of the display
            if len(row)+row_offset < WIDTH:
                if len(bitmap)+(col_offset//2) < HEIGHT:
                    if pixel == '1':
                        colour = fret_colours[col_offset//2]
                        display.set_pen(colour)
                        # set the game state
                    
                        if x+row_offset == 50:
#                             print(f'y+col_offset: {y+col_offset}')
                            if y+col_offset == 0: fret_e = True
                            if y+col_offset == 2: fret_d = True
                            if y+col_offset == 4: fret_c = True
                            if y+col_offset == 6: fret_b = True
                            if y+col_offset == 8: fret_a = True
                    else:
                        display.set_pen(black)

                    # display the pixel, double width
                    display.pixel(x+row_offset, y+col_offset)
                    display.pixel(x+row_offset, y+col_offset+1)
                    
                    
                          
            fret_no += 1
            row_offset += 2 
        col_offset += 2
        
def display_board():
    """ Display the gameboard """
    display.set_pen(white)
    display.line(50,0,50,11)
    display.update()
        
def fret_debug():
    if fret_a:
        display.set_pen(yellow)
        display.pixel(0,0)
    else:
        display.set_pen(black)
        display.pixel(0,0)
    if fret_b:
        display.set_pen(yellow)
        display.pixel(1,0)
    else:
        display.set_pen(black)
        display.pixel(1,0)
    if fret_c:
        display.set_pen(yellow)
        display.pixel(2,0)
    else:
        display.set_pen(black)
        display.pixel(2,0)
    if fret_d:
        display.set_pen(yellow)
        display.pixel(3,0)
    else:
        display.set_pen(black)
        display.pixel(3,0)
    if fret_e:
        display.set_pen(yellow)
        display.pixel(4,0)
    else:
        display.set_pen(black)
        display.pixel(4,0)
    display.update()
        
    
def check_buttons():
    """ Check the buttons on the Galactic Unicorn """
    win = True
    button_a = GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN
    button_b = GalacticUnicorn.SWITCH_BRIGHTNESS_UP
    button_c = GalacticUnicorn.SWITCH_SLEEP
    button_d = GalacticUnicorn.SWITCH_VOLUME_DOWN
    button_e = GalacticUnicorn.SWITCH_VOLUME_UP
    
    # if gu.is_pressed(button_a):
    #     print('button a pressed')
    # if gu.is_pressed(button_b):
    #     print('button b pressed')
    # if gu.is_pressed(button_c):
    #     print('button c pressed')
    # if gu.is_pressed(button_d):
    #     print('button d pressed')
    # if gu.is_pressed(button_e):
    #     print('button e pressed')
    
    tests = {fret_a:button_a, fret_b:button_b, fret_c:button_c, fret_d:button_d, fret_e:button_e}

    for fret, button in tests.items():
        if fret:
            if gu.is_pressed(button):
                win = True
            else:
                win = False
                break
    

    return win

def check_missed():
    """ Check if the note passed the bridge without a button being pressed """
    if fret_a or fret_b or fret_c or fret_d or fret_e:
        display.set_pen(red)
        display.rectangle(50,0,1,11)
        return True
    else:
        return False

# Transpose the tune
tune = transpose(tune)

# Set the starting position of the tune
x_reset = -len(tune[0]*2)
x = x_reset
y = 0

winning = True
lives = 3
while lives >= 0 :
    display.set_pen(black)
    display.clear()
    display_board()
    display_tune(tune,x,y)
#     fret_debug()
    check_missed()
    winning = check_buttons()
    if not winning:
        lives -= 1
    print(f'winning:{winning}')
    x = x + 1
    gu.update(display)
    sleep(0.01)
    offset = x - len(tune[0])
    if offset > WIDTH-4:
        x = x_reset
    
print("you lost")