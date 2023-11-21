class Diamond:
    def __init__(self, color, x4=False, x5=False):
        self.color = color
        self.x4 = x4
        self.x5 = x5
        self.x_position = None
        self.y_position = None

    def __del__(self):
        pass

    def upgrade_x4(self):
        self.x4 = True
        if self.x5:
            self.x5 = False

    def upgrade_x5(self):
        self.x5 = True
        if self.x4:
            self.x4 = False

    def push_x4(self):  # TODO add explode in sign +
        assert self.x4

    def push_x5(self):  # TODO add explode of all diamonds in same color
        assert self.x5
