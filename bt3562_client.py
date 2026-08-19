import random

class BT3562Client:
    def __init__(self, ip):
        self.ip = ip

    def connect(self):
        return True

    def read(self):
        v = round(3.55 + random.random() * 0.05, 3)
        ir = round(1.5 + random.random() * 0.5, 2)
        return f"{v},{ir}"