from panda3d.core import loadPrcFile 
loadPrcFile("config/conf.prc")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from direct.task.Task import Task
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay

import sys

# constants
Y_CON = 45     
SPEED = 3
#with my conf at 1000x600, the grid is like 20x12 ish
#possible colors: red__ blue_ green yello white

class ColorMaze(ShowBase):
    
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        super().__init__()
        #disables default mouse controls
        self.disableMouse()

        #creates a shape objects and renders them to this game
        player = Shape("shapemodels/whitesquare.egg", 0, 0, self.loader, self.render, "white")
        red_obs = Shape("shapemodels/red__rect.egg", 12, 3, self.loader, self.render, "red__")
        blue_obs = Shape("shapemodels/blue_rect.egg", -12, 3, self.loader, self.render, "blue_")
        green_obs = Shape("shapemodels/greenrect.egg", 4, 3, self.loader, self.render, "green")
        yellow_obs = Shape("shapemodels/yellorect.egg", -4, 3, self.loader, self.render, "yello")

        background = Shape("shapemodels/background.egg", 0, 0, self.loader, self.render, "backg", Y_CON+1)
        goal = Shape("shapemodels/goal_.egg", 0, 10, self.loader, self.render, "goal_")
        right_edge = Shape("shapemodels/horizontaledge.egg", 20, 0, self.loader, self.render, "horiz")
        left_edge = Shape("shapemodels/horizontaledge.egg", -20, 0, self.loader, self.render, "horiz")
        bottom_edge = Shape("shapemodels/verticaledge.egg", 0, -12, self.loader, self.render, "verti")

        #accepts keyboard input that calls the updater within the shape
        self.accept("arrow_left", player.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", player.updateKeyMap, ["left", False])
        self.accept("arrow_right", player.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", player.updateKeyMap, ["right", False])
        self.accept("arrow_up", player.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", player.updateKeyMap, ["up", False])
        self.accept("arrow_down", player.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", player.updateKeyMap, ["down", False])

        queue = CollisionHandlerQueue()
        traverser = CollisionTraverser("my_traverser")
        base.cTrav = traverser
        # traverser.addCollider(player.collider, queue)
        # traverser.traverse(render)

        #trav.showCollisions(self.render)
        # for entry in queue.entries:
        #     print(entry)

        #sets the move() in the shape to loop and do its job (move based on keyboard input)
        self.taskMgr.add(player.move, "move")

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
    def __init__(self, model, x, z, loader, render, color, y=Y_CON, collider=None):
        self.shape = loader.loadModel(model) 
        self.model = model
        self.x = x
        self.y = y
        self.z = z
        self.color = self.check_color(color)

        self.collider = collider
        # self.collider.reparentTo(self)

        self.shape.reparentTo(render)
        self.shape.setPos(x, y, z)

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

    #configured to check for colorfiles color specifically for files
    #shapemodels/XXXXX where the X's are the color
    def check_color(self, color):
        if color == self.model[12:17]:
            return color
        else:
            print("Color Image and Color code do not match")
            print(self.model[12:17], color)


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