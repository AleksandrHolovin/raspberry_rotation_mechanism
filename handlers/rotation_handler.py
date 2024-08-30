import time

class AngleHandler:
    def __init__(self):
        self.azimuth_angle = 0
        self.rotation_speed = 22.5  # degrees per second
        self.start_time = None
        self.direction = None

    def start_tracking(self, direction):
        self.direction = direction
        self.start_time = time.time()

    def stop_tracking(self):
        if self.start_time is None:
            return

        elapsed_time = time.time() - self.start_time
        angle_change = self.rotation_speed * elapsed_time

        if self.direction == 'left':
            self.azimuth_angle -= angle_change
        elif self.direction == 'right':
            self.azimuth_angle += angle_change

        self.azimuth_angle %= 360  # Ensure angle stays within 0-359 degrees
        self.start_time = None
        self.direction = None

    def get_angle(self):
        return self.azimuth_angle
