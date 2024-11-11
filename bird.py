from pico2d import load_image
from state_machine import *
from ball import Ball
import game_world
import game_framework
from random import randint

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KMPH = 100.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 100.0 / 6.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 15


#   100km/h, 50x50, 날개짓 초 당 5회
class Fly:
    @staticmethod
    def enter(bird, e):
        bird.action = 2
        bird.dir = 1
        bird.face_dir = 1
        bird.frame = 0

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (
            bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        ) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if bird.frame == 4:
            if bird.action == 2:
                bird.frame = 0
                bird.action = 1

            elif bird.action == 1:
                bird.frame = 0
                bird.action = 0

        elif bird.frame == 3 and bird.action == 0:
            bird.frame = 0
            bird.action = 2

        if bird.x > 1575:
            bird.face_dir = -1
            bird.dir = -1

        elif bird.x < 25:
            bird.face_dir = 1
            bird.dir = 1

    @staticmethod
    def draw(bird):
        if bird.dir > 0:
            bird.image.clip_draw(
                int(bird.frame) * 183,
                bird.action * 168,
                180,
                168,
                bird.x,
                bird.y,
                50,
                50,
            )

        else:
            bird.image.clip_composite_draw(
                int(bird.frame) * 183,
                bird.action * 168,
                180,
                168,
                0,
                "h",
                bird.x,
                bird.y,
                50,
                50,
            )
        print(f"b d: {bird.frame}")


class Bird:
    def __init__(self):
        self.x, self.y = randint(25, 250), 500
        self.face_dir = 1
        self.image = load_image("bird_animation.png")
        self.state_machine = StateMachine(self)
        self.state_machine.start(Fly)
        self.state_machine.set_transitions({})

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(("INPUT", event))

    def draw(self):
        self.state_machine.draw()
