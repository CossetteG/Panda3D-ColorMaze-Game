'''
ColorMaze
This is my final project for CS 1410
Built with Python using Panda3D

How to play:
    run main
    enter 1, 2, 3, or 4 in the terminal to choose the color of your player
    *once the game loads, use the up, down, left and right keys on your keyboard to move around
    only move through empty space or obstacles with the same color as you
    if you run into an obstacle of not your color, you will lose
    make your way upwards towards the goal(white)
    **don't go out of bounds (black)
    if you make it to the goal, you win
    close the program after winning or losing

Known bugs:
    *it doesn't automatically set as the foreground window so you will have to click over to the game
    **the bounds objects are supposed to stop you but it just clips through
'''

#get congiguration
from panda3d.core import loadPrcFile 
loadPrcFile("config/conf.prc")

#import all the Panda3d that I'm using
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import LPoint3, LVector3
from direct.task.Task import Task
from panda3d.core import CollisionTraverser, CollisionPolygon, CollisionNode, CollisionBox
from panda3d.core import CollisionHandlerEvent, CollisionRay, CollisionHandlerPusher
from panda3d.core import NodePath
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
import sys

# constants
Y_CON = 45     
SPEED = 3
#with my conf at 1000x600, the grid is like 20x12 ish
#possible colors: red__ blue_ green yello white

class ColorMaze(ShowBase):
    def __init__(self):
        #getting a color for the player
        code = getcolorcode()

        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        super().__init__()

        #disables default mouse controls
        self.disableMouse()

        #actually creating the player
        self.playermodel = "shapemodels/" + code + "square.egg"
        player = Shape(self.playermodel, 0, 0, self.loader, self.render, code, "player")
        
        #creates other shape objects and renders them to this game        
        red_obs = Shape("shapemodels/red__rect.egg", 12, 3, self.loader, self.render, "red__", "obs")
        blue_obs = Shape("shapemodels/blue_rect.egg", -12, 3, self.loader, self.render, "blue_", "obs")
        green_obs = Shape("shapemodels/greenrect.egg", 4, 3, self.loader, self.render, "green", "obs")
        yellow_obs = Shape("shapemodels/yellorect.egg", -4, 3, self.loader, self.render, "yello", "obs")

        background = Shape("shapemodels/background.egg", 0, 0, self.loader, self.render, "backg", "bg", Y_CON+1)
        goal = Shape("shapemodels/goal_.egg", 0, 10, self.loader, self.render, "goal_", "goal")
        right_edge = Shape("shapemodels/horizontaledge.egg", 20, 0, self.loader, self.render, "horiz", "h_edge")
        left_edge = Shape("shapemodels/horizontaledge.egg", -20, 0, self.loader, self.render, "horiz", "h_edge")
        bottom_edge = Shape("shapemodels/verticaledge.egg", 0, -12, self.loader, self.render, "verti", "v_edge")

        #accepts keyboard input that calls the updater within the shape
        self.accept("arrow_left", player.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", player.updateKeyMap, ["left", False])
        self.accept("arrow_right", player.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", player.updateKeyMap, ["right", False])
        self.accept("arrow_up", player.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", player.updateKeyMap, ["up", False])
        self.accept("arrow_down", player.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", player.updateKeyMap, ["down", False])
        
        #creates a text object to be updated later
        text = OnscreenText(text = " ", pos = (0, -.5), scale = .3)

        #creating events
        event = CollisionHandlerEvent()
        events = Events(event, player, text)
        pusher = CollisionHandlerPusher()

        #adds normal Collision events to everything that touches the player
        event.addInPattern('player-into-obs')
        base.cTrav = CollisionTraverser("player-into-obs")
        base.cTrav.addCollider(player.Col, event)

        #adds a special collider to each boundary object so player dont pass through
        base.cTrav.addCollider(left_edge.Col, pusher)
        pusher.addCollider(left_edge.Col, player.shape, base.drive.node()) 
        base.cTrav.addCollider(right_edge.Col, pusher)
        pusher.addCollider(right_edge.Col, player.shape, base.drive.node()) 
        base.cTrav.addCollider(bottom_edge.Col, pusher)
        pusher.addCollider(bottom_edge.Col, player.shape, base.drive.node()) 

        #tells the game to accept the event and run the handler
        self.accept("player-into-obs", events.handleRailCollision)

        #sets the move() in the shape to loop and do its job (move based on keyboard input)
        self.taskMgr.add(player.move, "move")

        

#the event handler object
class Events(DirectObject):
    def __init__(self, event, player, text):
        self.accept(event.addInPattern('%fn-into-%in'), self.handleRailCollision)
        self.player = player
        self.text = text

    #the player object and the text objects are passed in so they can be updated
    #chooses between printing brownie points, updating the text to you win or you lose,
    #freezes the shape
    def handleRailCollision(self, entry):
        obs_colors = ["green", "red__", "blue_", "yello"]
        into = str(entry.getIntoNodePath())[7:12]
        fromm = str(entry.getFromNodePath())[7:12]
        if fromm == into:
            print("brownie points!")
        elif into in obs_colors:
            self.text.text = "You Lose :("
            self.player.freeze()
        elif into == "goal_":
            self.text.text = ("You Win!")
            self.player.freeze()
        else:
            pass
        

class Shape():
    KeyMap = {
        "up": False, 
        "down": False, 
        "left": False, 
        "right": False
}
#box = CollisionBox(Point3(minx, miny, minz), Point3(maxx, maxy, maxz))
#"player": [Point3(-1, 0, -1), Point3(1, 0, 1)]
# "obs": [Point3(-2, 0, -1), Point3(2, 0, 1)],
# "bg": [Point3(-1, 5, -1), Point3(1, 5, 1)],
# "goal": [Point3(-20, 0, -.75), Point3(20, 0, .75)],
# "h_edge": [Point3(-.5, 0, -12), Point3(.5, 0, 12)],
# "v_edge": [Point3(-20, 0, -.5), Point3(20, 0, .5)]
#^this mess will tell you how much I struggled to get all the collider peices to work haha
    ColliderMap = {
        "player": [1, 1, 1],
        "obs": [3, 1, 1],
        "bg": [.5, .5, .5],
        "goal": [20, 1, .75],
        "h_edge": [.5, 2, 12],
        "v_edge": [20, 2, .5]
}
    
    #model is the egg file, render is passed through as a parameter but it's the game's render, 
    # and the game is 2d so we won't really use y
    def __init__(self, model, x, z, loader, render, color, character, y=Y_CON, freeze = False):
        self.shape = loader.loadModel(model) 
        self.model = model
        self.x = x
        self.y = y
        self.z = z
        self.color = self.check_color(color, self.model[12:17])
        self.character = character
        self._freeze = freeze

        dimn = self.ColliderMap[character]
        self.collider = CollisionBox(LPoint3(0, 0, 0), dimn[0], dimn[1], dimn[2])
        self.cnodePath = CollisionNode('cnode')
        self.cnodePath.addSolid(self.collider)
        self.Col = self.shape.attachNewNode(self.cnodePath)

        # self.cnodePath.node().setFromCollideMask(self.shape.getDefaultCollideMask())
        # self.cnodePath.setCollideMask(self.cnodePath.getCollideMask())
        self.Col.reparentTo(self.shape)
        # self.Col.show()

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
    def check_color(self, color, path):
        if color == path:
            return color
        else:
            print("Color Path and Color code do not match")
            print(path, color)

    def freeze(self):
        self._freeze = True

    #the function that is looped every frame to move the shape
    def move(self, task):
        if self._freeze == False:
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

#will ask the player which color they want to play
def getcolorcode():
    while True:
        num = input("Choose a color: 1 for red, 2 for blue, 3 for green, 4 for yellow: ")
        if num == '1':
            return "red__"
        elif num == '2':
            return "blue_"
        elif num == '3':
            return "green"
        elif num == '4':
            return "yello"
        else:
            pass

#LETS GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
def main():
    colormaze = ColorMaze()
    colormaze.run()


main()
# python3 colormaze/main.py
# save ur work before trying to run it babe