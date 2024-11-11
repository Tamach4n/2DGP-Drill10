from pico2d import load_image
from state_machine import *
from ball import Ball
import game_world
import game_framework

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KMPH = 100.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 100.0 / 6.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


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
        ) % 8
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

    @staticmethod
    def draw(bird):
        bird.image.clip_draw(
            int(bird.frame) * 100, bird.action * 168, 50, 50, bird.x, bird.y
        )
        print(f"b d: {bird.frame}")


class Bird:
    def __init__(self):
        self.x, self.y = 200, 500
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
