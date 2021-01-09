class figure:

    def __init__(self, color='white'):
        self.color = color


    def change_color(self, new_color):
        self.color = new_color
    

class oval(figure):

    def __init__(self, r1, r2, color='white'):
        figure.__init__(self, color)
        self.r1 = r1
        self.r2 = r2


class square(figure):

    def __init__(self, a, color='white'):
        figure.__init__(self, color)
        self.a = a
