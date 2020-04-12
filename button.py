class Button:
    def __init__(self, rect, text, is_active=True):
        self.rect = rect
        self.text = text
        self.is_active = is_active

    def is_inside(self, pos):
        if self.is_active:
            return self.rect.left < pos[0] < self.rect.right and self.rect.top < pos[1] < self.rect.bottom
        else:
            return False

    def switch(self):
        self.is_active = not self.is_active

    def disable(self):
        self.is_active = False

    def enable(self):
        self.is_active = True
