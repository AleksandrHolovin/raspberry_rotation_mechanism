# angle_handler.py
import time

class RotationHandler:
    def __init__(self):
        self.azimuth_angle = 0
        self.angle_change_per_second = 22.5  # 90 degrees / 4 seconds
        self.start_time = None
        self.direction = None

    def start_tracking(self, direction):
        self.direction = direction
        self.start_time = time.time()

    def update_angle(self):
        if self.start_time is None or self.direction is None:
            return

        elapsed_time = time.time() - self.start_time
        angle_change = self.angle_change_per_second * elapsed_time

        if self.direction == 'left':
            self.azimuth_angle -= angle_change
        elif self.direction == 'right':
            self.azimuth_angle += angle_change

        self.azimuth_angle = self.azimuth_angle % 360  # Keep angle within 0-360 degrees

    def stop_tracking(self):
        self.start_time = None
        self.direction = None

    def get_angle(self):
        self.update_angle()
        return self.azimuth_angle
