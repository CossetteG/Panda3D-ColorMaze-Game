from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from panda3d.core import SamplerState
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait, Func
import sys

from shapes import Shape


class ColorMaze(ShowBase):
    print("check1")
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        my_shape = Shape("/samples/asteroids/textures/asteroid1.png", (0, 0), "blue", None, None, None)
        self.loadedshape = my_shape.load_object()
    
    print("check2")

    def genLabelText(text, i):
        return OnscreenText(text=text, parent=base.a2dTopRight, pos=(0.07, -.06 * i - 0.1),
                            fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)


def main():
    print("check0")
    ColorMaze.run()



main()
# python3 colormaze/main.py
# save ur work before trying to run it babe