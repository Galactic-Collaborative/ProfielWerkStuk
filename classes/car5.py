import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x:int, y:int):
        self.wheel_base = 70
        self.steering_angle = 15
        self.engine_power = 800
        self.friction = -0.9
        self.drag = -0.001
        self.braking = -450
        self.max_speed_reverse = 250
        self.slip_speed = 400
        self.traction_fast = 0.1
        self.traction_slow = 0.7
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.steer_direction = 0
        self.position = Vector2D(0,0)

    def draw(self, batch):
        car = self.drawCar(batch)
        return car

    def drawCar(self, batch):
        car = pyglet.sprite.Sprite(pyglet.resource.image('img/car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.rotation)
        return car

    def _physics_process(self, dt, key, key_handler):
        # self.acceleration = Vector2.ZERO
        self.get_input(key, key_handler)
        # self.apply_friction()
        self.calculate_steering(dt)
        self.velocity += acceleration * dt
        # self.velocity = move_and_slide(self.velocity)

    def apply_friction():
        if self.velocity.length() < 5:
            # self.velocity = Vector2.ZERO
        friction_force = self.velocity * self.friction
        drag_force = self.velocity * self.velocity.length() * self.drag
        self.acceleration += drag_force + friction_force

    def get_input(self, key, key_handler):
        turn = 0
        if key_handler[key.LEFT]:
            turn -= 1
        if key_handler[key.RIGHT]:
            turn += 1

        self.steer_direction = turn * self.steering_angle

        if key_handler[key.UP]:
        #     self.acceleration = transform.x * self.engine_power
        if key_handler[key.DOWN]:
        #     self.acceleration = transform.x * self.braking

    def calculate_steering(self, dt):
        # rear_wheel = self.position - transform.x * self.wheel_base/2
        # front_wheel = self.position + transform.x * self.wheel_base/2
        rear_wheel += self.velocity * dt
        front_wheel += self.velocity.rotate(self.steer_direction) * dt
        new_heading = (front_wheel - rear_wheel).normalize()
        traction = self.traction_slow
        if self.velocity.length() > self.slip_speed:
            traction = self.traction_fast
        d = new_heading.dot(self.velocity.normalize(in_place=False))
        if d > 0:
            # self.velocity = self.velocity.linear_interpolate(new_heading * self.velocity.length(), traction)
        if d < 0:
            # self.velocity = -new_heading * min(self.velocity.length(), self.max_speed_reverse)
        self.rotation = new_heading.rotation()