class Rectangle:
    def __init__(self, h, w):
        self.h = h
        self.w = w
    
    @property
    def area(self):
        return self.h * self.w