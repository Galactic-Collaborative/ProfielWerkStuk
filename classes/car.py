import pyglet, math
from pyglet.gl import *
from Vector import Vector2D
from typing import NewType

key = pyglet.window.key
speed = 1.0

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.v_acceleration = Vector2D(0,0)
        self.v_velocity = Vector2D(0,0)
        self.rotation = 0
        self.limiet = 2
        self.limiet2 = -2

    def drawCar(self):
        car = pyglet.sprite.Sprite(pyglet.resource.image('car2.png'), x=self.position.x, y=self.position.y)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.rotation)
        car.draw()

    def drawInfo(self):
        self.labelA = pyglet.text.Label(str(self.v_acceleration.x), font_name='Times New Roman', font_size=36, x=50, y=950, anchor_x='left', anchor_y='center')
        self.labelA.draw()
        self.labelB = pyglet.text.Label(str(self.v_acceleration.y), font_name='Times New Roman', font_size=36, x=50, y=900, anchor_x='left', anchor_y='center')
        self.labelB.draw()
        self.labelC = pyglet.text.Label(str(self.rotation), font_name='Times New Roman', font_size=36, x=50, y=850, anchor_x='left', anchor_y='center')
        self.labelC.draw()
        self.labelD = pyglet.text.Label(str(self.v_velocity.x), font_name='Times New Roman', font_size=36, x=50, y=800, anchor_x='left', anchor_y='center')
        self.labelD.draw()
        self.labelE = pyglet.text.Label(str(self.v_velocity.y), font_name='Times New Roman', font_size=36, x=50, y=750, anchor_x='left', anchor_y='center')
        self.labelE.draw()
    #     self.labelV = pyglet.text.Label(self.v_velocity, font_name='Times New Roman', font_size=36, x=400, y=300, anchor_x='center', anchor_y='center')

    def forward(self):
        self.v_acceleration += Vector2D(1,0)

    def backward(self):
        self.v_acceleration -= Vector2D(1,0)

    def left(self):
        self.v_acceleration += Vector2D(0,0.1)

    def right(self):
        self.v_acceleration -= Vector2D(0,0.1)

    def update(self):
        self.v_velocity = self.v_acceleration 
        if self.v_velocity.x >= 0:
            self.rotation = self.v_velocity.rotation()
        else:
            self.rotation = 180-self.v_velocity.rotation()
        self.v_acceleration.limit(2)
        # if self.v_acceleration.x >= self.limiet:
        #     self.v_acceleration.x = self.limiet
        # if self.v_acceleration.x <= self.limiet2:
        #     self.v_acceleration.x = self.limiet2
        # if self.v_acceleration.y >= self.limiet:
        #     self.v_acceleration.y = self.limiet
        # if self.v_acceleration.y <= self.limiet2:
        #     self.v_acceleration.y = self.limiet2

        self.position += self.v_velocity
        
    def drive(self):
        self.test = 0


class main(pyglet.window.Window):
    def __init__ (self, width=1600, height=1000, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)
        self.x, self.y = 0, 0
        self.alive = 1

        self.CAR = Car(400, 300)
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.alive = 0

        if symbol == key.UP:
            self.up_pressed = True

        if symbol == key.DOWN:
            self.down_pressed = True

        if symbol == key.LEFT:
            self.left_pressed = True

        if symbol == key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.up_pressed = False

        if symbol == key.DOWN:
            self.down_pressed = False

        if symbol == key.LEFT:
            self.left_pressed = False

        if symbol == key.RIGHT:
            self.right_pressed = False

    def render(self):
        self.clear()

        self.CAR.drawCar()
        self.CAR.drawInfo()
        
        if self.up_pressed == True:
            self.CAR.forward()
        if self.down_pressed == True:
            self.CAR.backward()
        if self.left_pressed == True:
            self.CAR.left()
        if self.right_pressed == True:
            self.CAR.right()
        self.CAR.update()
            
        self.CAR.drive()
        self.flip()

    def run(self):
        while self.alive == 1:
            self.render()

            event = self.dispatch_events()

if __name__ == '__main__':
    x = main()
    x.run()