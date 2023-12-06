from panda3d.core import loadPrcFile 
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
# from panda3d.core import SamplerState
# from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
# from math import sin, cos, pi
# from random import randint, choice, random
# from direct.interval.MetaInterval import Sequence
# from direct.interval.FunctionInterval import Wait, Func
import sys

from shapes import Shape, CON

# constants
Y_CON = 15     


class ColorMaze(ShowBase):
    print("check1")
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        super().__init__()
        #disables default mouse controls
        self.disableMouse()

        
        square = Shape("shapemodels/plane.egg", 0, Y_CON, 0, self.loader, self.render)

    def genLabelText(text, i):
        return OnscreenText(text=text, parent=base.a2dTopRight, pos=(0.07, -.06 * i - 0.1),
                            fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)


class Shape():
    def __init__(self, model, x, y, z, loader, render):
        self.shape = loader.loadModel(model) 
        self.shape.setPos(x, y, z)
        self.shape.reparentTo(render)
    print("check2")





def main():
    colormaze = ColorMaze()
    colormaze.run()
    colormaze.load_shapes()


main()
# python3 colormaze/main.py
# save ur work before trying to run it babe