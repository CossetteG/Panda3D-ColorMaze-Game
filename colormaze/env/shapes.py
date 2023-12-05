from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from panda3d.core import SamplerState
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from math import sin, cos, pi
# from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait, Func
import sys

class Shape:
    obj = None

    print("check3")
    def __init__(self, model, start_pos, color, collider, mover, event):
        self.model = model
        self.pos = start_pos
        self.color = color
        self.collider = collider
        self.mover = mover
        self.event = event 

    #(tex=None, pos=LPoint3(0, 0), depth=SPRITE_POS, scale=1, transparency=True)
    def load_object(self, depth=55, scale=1, transparency = False):
        self.obj = loader.loadModel("models/plane")
        self.obj.reparentTo(camera)

        # Set the initial position and scale.
        self.obj.setPos(self.pos.getX(), depth, self.pos.getY())
        self.obj.setScale(scale)

        # This tells Panda not to worry about the order that things are drawn in
        # (ie. disable Z-testing).  This prevents an effect known as Z-fighting.
        self.obj.setBin("unsorted", 0)
        self.obj.setDepthTest(False)

        if transparency:
            self.obj.setTransparency(TransparencyAttrib.MAlpha)

        # Load and set the requested texture.
        tex = loader.loadTexture(self.model)
        tex.setWrapU(SamplerState.WM_clamp)
        tex.setWrapV(SamplerState.WM_clamp)
        self.obj.setTexture(tex, 1)

        print("check4")
        return self.obj


