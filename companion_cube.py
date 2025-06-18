import pyautogui
import tkinter as tk
import math
import pymunk
from PIL import Image, ImageTk

INITIAL_Y = 1040
GRAVITY = 2000              #(0, inf), > se >
ANGULAR_SENSIBILITY = 2.0   #(0, inf), > se <
SPEED_SCALE = 4             #(0, inf), > se >
MAX_QUEUE_SIZE = 10         #(0, inf)
SHAPE_FRICTION = 0.8        #[0, 1], > se >
FLOOR_FRICTION = 0.8        #[0, 1], > se >
SHAPE_ELASTICITY = 0.6      #[0, 1], > se > 0.5
FLOOR_ELASTICITY = 0.9        #[0, 1], > se >

class spriteObject:    
    def __init__(self, x, y):
        self.window = tk.Tk()
        self.x = x
        self.y = y

def dragStart(event):
    widget = event.widget
    widget._dragStart_x = event.x_root - cube.window.winfo_x()
    widget._dragStart_y = event.y_root - cube.window.winfo_y()
    cube.dragging = True

def dragMotion(event):
    x = event.x_root - label._dragStart_x
    y = event.y_root - label._dragStart_y
    cube.x = x
    cube.y = y
    cube.body.position = (x + 50, y + 50)
    cube.body.velocity = (0, 0)
    cube.window.geometry(f'+{x}+{y}')

def dragStop(event):
    cube.dragging = False

    dir_x = pos_q[-1][0] - pos_q[0][0]
    dir_y = pos_q[-1][1] - pos_q[0][1]
    angle = math.atan2(dir_y, dir_x)
    speed = math.sqrt(math.pow(dir_y, 2) + math.pow(dir_x, 2)) * SPEED_SCALE

    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    cube.body.velocity = (vx, vy)

    if len(pos_q) >= 3:
        dx1 = pos_q[-2][0] - pos_q[-3][0]
        dx2 = pos_q[-1][0] - pos_q[-2][0]
        angular_dir = (dx2 - dx1) / ANGULAR_SENSIBILITY
        cube.body.angular_velocity = angular_dir

def refresh():
    mouse_x = cube.window.winfo_pointerx()
    mouse_y = cube.window.winfo_pointery()
    pos_q.append((mouse_x, mouse_y))
    if len(pos_q) > MAX_QUEUE_SIZE:
        pos_q.pop(0)

    if not cube.dragging:
        space.step(1 / 60.0)
        x, y = cube.body.position
        angle_degrees = math.degrees(cube.body.angle) % 360

        if x < 0:
            x = cube.window.winfo_screenwidth()-1
        elif x > cube.window.winfo_screenwidth():
            x = 1
        if y > INITIAL_Y+50:
            y = INITIAL_Y+48
        cube.body.position = (x, y)
        cube.x = int(x - 50)
        cube.y = int(y - 50)
        
        rotated_sprite = sprite.rotate(-angle_degrees, resample=Image.BICUBIC)
        tk_rotated = ImageTk.PhotoImage(rotated_sprite)
        label.configure(image=tk_rotated)
        label.image = tk_rotated

        cube.window.geometry(f'200x200+{cube.x}+{cube.y-50}')
    
    cube.window.after(16, refresh)

cube = spriteObject(x=1400, y=INITIAL_Y-200)
cube.dragging = False

#crea space
space = pymunk.Space()
space.gravity = (0, GRAVITY)

#crea il body
mass = 10
size = 100
moment = pymunk.moment_for_box(mass, (size, size))
cube.body = pymunk.Body(mass, moment)
cube.body.position = (cube.x + 50, cube.y + 50)

shape = pymunk.Poly.create_box(cube.body, (size, size))
shape.elasticity = SHAPE_ELASTICITY
shape.friction = SHAPE_FRICTION
space.add(cube.body, shape)

#crea floor
floor = pymunk.Segment(space.static_body, (0, INITIAL_Y + 100), (1920, INITIAL_Y + 100), 1)
floor.elasticity = FLOOR_ELASTICITY
floor.friction = FLOOR_FRICTION
space.add(floor)

#window setup
cube.window.config(highlightbackground='black')
cube.window.overrideredirect(True)
cube.window.wm_attributes('-transparentcolor', 'black')
cube.window.wm_attributes("-topmost", 1)

label = tk.Label(cube.window, bd=0, bg='black')

sprite = Image.open("C:\\Users\\riccardo.benetti\\Documents\\Codici python\\companion cube\\companion_cube_sprite_big.png")
sprite = sprite.convert('RGBA')
tk_sprite = ImageTk.PhotoImage(sprite)

label.configure(image=tk_sprite)
label.image = tk_sprite

label.bind("<Button-1>", dragStart)
label.bind("<B1-Motion>", dragMotion)
label.bind("<ButtonRelease-1>", dragStop)
label.pack()

pos_q = []

cube.window.after(16, refresh)
cube.window.mainloop()
