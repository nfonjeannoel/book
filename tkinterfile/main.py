import tkinter
import xml.dom.minidom
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
import turtle

from turtlefile.main import PyList, CircleCommand, BeginFillCommand, EndFillCommand, PenUpCommand, PenDownCommand, \
    GoToCommand


class DrawingApplication(tkinter.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        self.graphicsCommands = PyList()

    def buildWindow(self):
        self.master.title("Draw")
        bar = tkinter.Menu(self.master)
        fileMenu = tkinter.Menu(bar, tearoff=0)

        def newWindow():
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0, 0)
            theTurtle.pendown()
            screen.update()
            screen.listen()
            self.graphicsCommands = PyList()

        def parse(fileName):
            xmldoc = xml.dom.minidom.parse(fileName)
            graphicsCommandsElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]
            graphicsCommands = graphicsCommandsElement.getElementsByTagName("Command")
            for commandElement in graphicsCommands:
                print(type(commandElement))
                print(commandElement)
                print()
                command = commandElement.firstChild.data.strip()


        def loadFile():
            filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")
            newWindow()
            self.graphicsCommands = PyList()
            parse(filename)
            for cmd in self.graphicsCommands:
                cmd.draw()

            screen.update()

        fileMenu.add_command(label="Load...", command=loadFile)

        def addToFile():
            filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")
            theTurtle.penup()
            theTurtle.goto(0, 0)
            theTurtle.pendown()
            theTurtle.pencolor("#000000")
            theTurtle.fillcolor("#000000")
            cmd = PenUpCommand()
            self.graphicsCommands.append(cmd)
            cmd = GoToCommand(0, 0, 1, "#000000")
            self.graphicsCommands.append(cmd)
            cmd = PenDownCommand()
            self.graphicsCommands.append(cmd)
            screen.update()
            parse(filename)

            for cmd in self.graphicsCommands:
                cmd.draw()

            screen.update()

        def write(fileName):
            with open(f"{fileName}.xml", "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
                file.write('<GraphicsCommands>\n')
                for cmd in self.graphicsCommands:
                    # overide the string method
                    file.write('   ' + str(cmd) + "\n")
                file.write('</GraphicsCommands>\n')

        def saveFile():
            fileName = tkinter.filedialog.asksaveasfilename(title="Save Picture as ...")
            write(fileName)

        fileMenu.add_command(label="New", command=newWindow)
        fileMenu.add_command(label="Load Into", command=addToFile)
        fileMenu.add_command(label="Save As...", command=saveFile)
        fileMenu.add_command(label="Exit", command=self.master.quit)
        bar.add_cascade(label="File", menu=fileMenu)
        self.master.config(menu=bar)

        canvas = tkinter.Canvas(self, width=600, height=600)
        canvas.pack(side=tkinter.LEFT)

        theTurtle = turtle.RawTurtle(canvas)
        theTurtle.shape(name='circle')
        # theTurtle.hideturtle()
        screen = theTurtle.getscreen()
        screen.tracer(0)

        sidebar = tkinter.Frame(self, padx=5, pady=5)
        sidebar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

        pointLabel = tkinter.Label(sidebar, text="Width")
        pointLabel.pack()

        widthSize = tkinter.StringVar()
        widthEntry = tkinter.Entry(sidebar, textvariable=widthSize)
        widthEntry.pack()
        widthSize.set(str(1))

        radiusLabel = tkinter.Label(sidebar, text="Radius")
        radiusLabel.pack()

        radiusSize = tkinter.StringVar()
        radiusEntry = tkinter.Entry(sidebar, textvariable=radiusSize)
        radiusSize.set(str(10))
        radiusEntry.pack()

        def circleHandler():
            cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())  # getPencolor
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

            screen.update()
            screen.listen()

        circleButton = tkinter.Button(sidebar, text="Draw Circle", command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)

        screen.colormode(255)
        penLabel = tkinter.Label(sidebar, text="Pen Color")
        penLabel.pack()

        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sidebar, textvariable=penColor)
        penEntry.pack()

        penColor.set("#000000")

        def getPenColor():
            color = tkinter.colorchooser.askcolor()
            if color is not None:
                penColor.set(str(color)[-9:-2])

        penColorButton = tkinter.Button(sidebar, text="Pick Pen Color", command=getPenColor)
        penColorButton.pack(fill=tkinter.BOTH)

        fillLabel = tkinter.Label(sidebar, text="Fill Color")
        fillLabel.pack()

        fillColor = tkinter.StringVar()
        fillEntry = tkinter.Entry(sidebar, textvariable=fillColor)
        fillEntry.pack()
        fillColor.set("#000000")

        def getFillColor():
            color = tkinter.colorchooser.askcolor()
            if color is not None:
                fillColor.set(str(color)[-9:-2])

        fillColorButton = tkinter.Button(sidebar, text="Pick Fill Color", command=getFillColor)
        fillColorButton.pack(fill=tkinter.BOTH)

        fillStatus = tkinter.Label(sidebar, text="Not Filling")
        fillStatus.pack()

        def beginFillHandler():
            fillStatus.configure(text="Currently Filling")
            cmd = BeginFillCommand(fillColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        beginFillButton = tkinter.Button(sidebar, text="Begin Fill", command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH)

        def endFillHandler():
            fillStatus.configure(text="Not Filling")
            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        endFillButton = tkinter.Button(sidebar, text="End Fill", command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH)

        penLabel = tkinter.Label(sidebar, text="Pen Is Down")
        penLabel.pack()

        def penUpHandler():
            cmd = PenUpCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Up")
            self.graphicsCommands.append(cmd)

        penUpButton = tkinter.Button(sidebar, text="Pen Up", command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH)

        def penDownHandler():
            cmd = PenDownCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Down")
            self.graphicsCommands.append(cmd)

        penDownButton = tkinter.Button(sidebar, text="Pen Down", command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)

        def clickHandler(x, y):
            cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        screen.onclick(clickHandler)

        def dragHandler(x, y):
            cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        theTurtle.ondrag(dragHandler)

        def redrawScreen():
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0, 0)
            theTurtle.pendown()

            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
            screen.update()
            screen.listen()

        def undoHandler():
            if len(self.graphicsCommands) > 0:
                self.graphicsCommands.removeLast()
                redrawScreen()

        def redoHandler():
            if self.graphicsCommands.historySize() > 0:
                self.graphicsCommands.setItems(self.graphicsCommands.allHistory()[:len(self.graphicsCommands) + 1])
                redrawScreen()

        bar.add_cascade(label="Redo", command=redoHandler)
        screen.onkeypress(redoHandler, "r")

        bar.add_cascade(label="Undo", command=undoHandler)
        screen.onkeypress(undoHandler, "u")
        screen.listen()


def main():
    root = tkinter.Tk()
    drawingApp = DrawingApplication(root)
    drawingApp.mainloop()


if __name__ == '__main__':
    main()
