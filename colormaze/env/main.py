from panda3d.core import loadPrcFile 
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from direct.task.Task import Task

import sys

# constants
Y_CON = 45     
SPEED = 3
#with my conf at 1000x600, the grid is like 18x12 ish


class ColorMaze(ShowBase):
    
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        super().__init__()
        #disables default mouse controls
        self.disableMouse()

        #creates a shape object and renders it to this game
        square = Shape("shapemodels/whitesquare.egg", 0, 0, self.loader, self.render)
        square.set_position(0, 0)

        #accepts keyboard input that calls the updater within the shape
        self.accept("arrow_left", square.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", square.updateKeyMap, ["left", False])
        self.accept("arrow_right", square.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", square.updateKeyMap, ["right", False])
        self.accept("arrow_up", square.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", square.updateKeyMap, ["up", False])
        self.accept("arrow_down", square.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", square.updateKeyMap, ["down", False])

        #sets the move() in the shape to loop and do its job (move based on keyboard input)  
        self.taskMgr.add(square.move, "move")

    #copied. idk yet but its not breaking anything
    def genLabelText(text, i):
        return OnscreenText(text=text, parent=base.a2dTopRight, pos=(0.07, -.06 * i - 0.1),
                            fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)


class Shape():
    KeyMap = {
    "up": False, 
    "down": False, 
    "left": False, 
    "right": False
}
    #model is the egg file, render is passed through as a parameter but it's the game's render, 
    # and the game is 2d so we won't really use y
    def __init__(self, model, x, z, loader, render, y=Y_CON):
        self.shape = loader.loadModel(model) 
        self.x = x
        self.y = y
        self.z = z
        self.shape.reparentTo(render)

    #used to change the position of the shape at any time
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

    #the function that is looped every frame to move the shape
    def move(self, task):
        #get the current values for position and time
        dt = globalClock.getDt()
        new_x = self.get_x()
        new_z = self.get_z()

        #check the map for keyboard input and update position values as necessary
        if self.KeyMap["left"] == True:
            new_x -= SPEED*dt
        
        if self.KeyMap["right"] == True:
            new_x += SPEED*dt
       
        if self.KeyMap["up"] == True:
            new_z += SPEED*dt
        
        if self.KeyMap["down"] == True:
            new_z -= SPEED*dt
        
        #set the new position with the updated values and loop
        self.set_position(new_x, new_z)
        return task.cont

    #a helper function to update values for move() to use
    def updateKeyMap(self, key, state):
        self.KeyMap[key] = state


def main():
    colormaze = ColorMaze()
    colormaze.run()


main()
# python3 colormaze/main.py
# save ur work before trying to run it babe