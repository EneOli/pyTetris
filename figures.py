class Figure:
    def __init__(self):
        # OVERRIDE!
        self.body = [
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ]
        self.x = 1
        self.y = 1
        self.rotation = 0

    def rotate(self):
        new_lines = []
        for x in range(len(self.body[0])):
            line = []
            for y in reversed(range(len(self.body))):
                line.append(self.body[y][x])
            new_lines.append(line)
        self.body = new_lines

    def get_lowest_y(self):
        return self.y + len(self.body) - 1

    def get_left_x(self):
        return self.x

    def get_right_x(self):
        return self.x + len(self.body[0]) - 1


class L(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (1, 0),
            (1, 0),
            (1, 0),
            (1, 1)
        ]


class I(Figure):
    def __init__(self):
        super().__init__()
        # force tuple
        self.body = [
            (1,),
            (1,),
            (1,),
            (1,)
        ]


class L2(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (1, 1),
            (1, 0),
            (1, 0),
            (1, 0)
        ]


class S(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (1, 0),
            (1, 1),
            (0, 1),
        ]


class S2(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (0, 1),
            (1, 1),
            (1, 0),
        ]


class B(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (1, 1),
            (1, 1),
        ]


class T(Figure):
    def __init__(self):
        super().__init__()
        self.body = [
            (0, 1, 0),
            (1, 1, 1)
        ]
