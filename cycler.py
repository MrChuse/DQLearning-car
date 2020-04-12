class Cycler:

    def __init__(self, buttons):
        self.buttons = buttons
        self.buttons[0].enable()
        for button in buttons[1:]:
            button.disable()
        self.counter = 0

    def is_inside(self, pos):
        if self.buttons[self.counter].is_inside(pos):
            self.buttons[self.counter].disable()
            self.counter = (self.counter + 1) % len(self.buttons)
            self.buttons[self.counter].enable()
            return True
        return False

    def get_active_button(self):
        return self.buttons[self.counter]
