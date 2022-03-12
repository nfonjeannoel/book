import turtle


class GoToCommand:
    def __init__(self, x, y, width=1, color="black"):
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)


class CircleCommand:
    def __init__(self, radius, width=1, color="black"):
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)


class BeginFillCommand:
    def __init__(self, color):
        self.color = color

    def draw(self, turtle_):
        turtle_.fillcolor(self.color)
        turtle_.begin_fill()


class EndFillCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.end_fill()


class PenUpCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.penup()


class PenDownCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.pendown()


class PyList:
    history = []

    def __init__(self):
        self.items = []
        self.history = []

    def allHistory(self):
        return self.history

    def historySize(self):
        return len(self.history)

    def setItems(self, items):
        self.items = items

    def append(self, item):
        self.items = self.items + [item]
        self.history = self.history + [item]

    def __iter__(self):
        for c in self.items:
            yield c

    def __len__(self):
        return len(self.items)

    def removeLast(self):
        self.items = self.items[:-1]


def main():
    filename = input("Please enter drawing filename: ")
    t = turtle.Turtle()
    screen = t.getscreen()
    file = open(filename, "r")
    # Create a PyList to hold the graphics commands that are
    # read from the file.
    graphicsCommands = PyList()
    command = file.readline().strip()
    while command != "":
        if command == "goto":
            x = float(file.readline())
            y = float(file.readline())
            width = float(file.readline())
            color = file.readline().strip()
            cmd = GoToCommand(x, y, width, color)
        elif command == "circle":
            radius = float(file.readline())
            width = float(file.readline())
            color = file.readline().strip()
            cmd = CircleCommand(radius, width, color)
        elif command == "beginfill":
            color = file.readline().strip()
            cmd = BeginFillCommand(color)
        elif command == "endfill":
            cmd = EndFillCommand()

        elif command == "penup":
            cmd = PenUpCommand()

        elif command == "pendown":
            cmd = PenDownCommand()

        else:
            raise RuntimeError("Unknown Command " + command)

        graphicsCommands.append(cmd)
        command = file.readline().strip()

    for cmd in graphicsCommands:
        cmd.draw(t)

    file.close()
    t.ht()
    screen.exitonclick()


if __name__ == '__main__':
    main()
#
# def main():
#     file_name = input("enter filename: ")
#
#     t = turtle.Turtle()
#     screen = t.getscreen()
#     with open(file_name, 'r') as file:
#         for line in file:
#             text = line.strip()
#
#             command_list = text.split(",")
#             command = command_list[0]
#
#             if command == "goto":
#                 x = float(command_list[1])
#                 y = float(command_list[2])
#                 width = float(command_list[3])
#                 color = command_list[4].strip()
#                 t.width(width)
#                 t.pencolor(color)
#                 t.goto(x, y)
#
#             elif command == "circle":
#                 radius = float(command_list[1])
#                 width = float(command_list[2])
#                 color = command_list[3].strip()
#                 t.width(width)
#                 t.pencolor(color)
#                 t.circle(radius)
#             elif command == "beginfill":
#                 color = command_list[1].strip()
#                 t.fillcolor(color)
#                 t.begin_fill()
#             elif command == "endfill":
#                 t.end_fill()
#             elif command == "penup":
#                 t.penup()
#             elif command == "pendown":
#                 t.pendown()
#             else:
#                 print("Unknown command found in file:", command)
#
#     t.hideturtle()
#     screen.exitonclick()


# if __name__ == '__main__':
#     main()
