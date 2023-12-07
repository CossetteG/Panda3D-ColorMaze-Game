from panda3d.core import loadPrcFile 
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3

from direct.task.Task import Task

import sys

# constants
Y_CON = 45     


class ColorMaze(ShowBase):
    
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        super().__init__()
        #disables default mouse controls
        self.disableMouse()

        square = Shape("shapemodels/whitesquare.egg", 0, 0, self.loader, self.render)
        square.set_position(3, -3)
        
        active = square
        self.taskMgr.add(square.move, "move")

    
    def genLabelText(text, i):
        return OnscreenText(text=text, parent=base.a2dTopRight, pos=(0.07, -.06 * i - 0.1),
                            fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)




class Shape():
    def __init__(self, model, x, z, loader, render, y=Y_CON):
        self.shape = loader.loadModel(model) 
        self.x = x
        self.y = y
        self.z = z
        self.shape.reparentTo(render)

    def set_position(self, new_x, new_z, new_y=Y_CON):
        self.shape.setPos(new_x, new_y, new_z)
        self.x = new_x
        self.y = new_y
        self.z = new_z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def move(self, task):
        x_rate = .1
        z_rate = .1
        if self.get_x() >= 5:
            return task.done
        else:
            new_x = self.get_x() + x_rate
            new_z = self.get_z() + z_rate
            self.set_position(new_x, new_z)
            print(self.get_x())
            return task.cont


def main():
    colormaze = ColorMaze()
    colormaze.run()
    colormaze.load_shapes()


main()
# python3 colormaze/main.py
# save ur work before trying to run it babe