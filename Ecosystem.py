# START FILE
#=======================================================================
# GENERAL DOCUMENTATION ------------------------------------------------
""" 
"""

# ADDITIONAL DOCUMENTATION ---------------------------------------------

# Modification History:
# - 3 Mar 2020: File Created

# Notes:
# - Written for Python 3.7
# - To test simply run the file in the canopy distribution of python
#  or through some other IDE like visual studio or spyder
# - Documentation style inspired by CSS 458 professor Johnny Lin

#=======================================================================
# PROGRAM IMPORTS ------------------------------------------------------
import numpy as nu
import matplotlib.pyplot as plt
import Fauna as fa
import Flora as fo

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

GRID_X = 50                     # var meaning
GRID_Y = 50

# PROGRAM GLOBALS ------------------------------------------------------
# Not User Modifiable

var = 0                     # var meaning

#=======================================================================
# CLASS: Ecosystem -----------------------------------------------------
class EcoSystem:
    """ Description:
    
        Variables: 
        -var: 
    
        Methods: 
    """
    frame = None
    lenght = None
    width = None
    
    
    
    # MEATHOD: INIT ----------------------------------------------------
    def __init__(self):
        """ Description: Class constructor
            
    
            Variables: 
            -var: 
    
            Output: 
        """
        self.frame = 1

        #Grid Size variables
        self.length = 50
        self.width = 50
        
        # These grids track constant values accross the grid
        self.light_grid = nu.ones((self.length, self.width))
        self.water_grid = nu.zeros((self.length, self.width))
        self.temp_grid = nu.zeros((self.length, self.width))

        # These grids are booleans(0/1) for when animals are at a location
        self.plant_grid = nu.zeros((self.length, self.width))
        self.herbivore_grid = nu.zeros((self.length, self.width))
        self.carnivore_grid = nu.zeros((self.length, self.width))
        
        # These lists hold every individual plant and animal
        self.plant_list = []
        self.herbivore_list = []
        self.carnivore_list = []
        
        self.initPlants()
        self.initRabbits()
        
    # MEATHOD: displayGrid ---------------------------------------------
    def displayFrame(self):
        """ Description: displays a frame from the simulation
            
            Variables: 
                -self: the SimGrid object instance
        """
        # get boarder values of rgb grid
        simFrame = nu.full((self.length+2, self.width+2, 3), [0.3, 0.3, 0])
        simFrame[0, :, :] = [0, 0, 0]
        simFrame[-1, :, :] = [0, 0, 0]
        simFrame[:, -1, :] = [0, 0, 0]
        simFrame[:, 0, :] = [0, 0, 0]
        
        # get interior values of rgb grid
        shape = nu.shape(simFrame)
        for y in range(1,shape[0]-1):
            for x in range(1,shape[1]-1):
                if(self.carnivore_grid[y-1,x-1] == 1):
                    simFrame[y, x, :] = [0.8, 0.4, 0]
                elif(self.herbivore_grid[y-1,x-1] == 1):
                    simFrame[y, x, :] = [1, 1, 1] 
                elif(self.plant_grid[y-1,x-1] == 1):
                    simFrame[y, x, :] = [0, 0.6, 0]

        # formatting
        plt.title("EcoSystem Simulation Frame: " + str(self.frame))
        plt.axis("off")
        plt.imshow(simFrame)
        plt.pause(0.5)

    # MEATHOD: displayGrid ---------------------------------------------
    def displayGrid(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        
        cm = ['YlOrBr_r', 'Blues', 'RdBu_r']
        
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.light_grid,
                            cmap=cm[0])
        fig.colorbar(pcm, ax=axs)
        #ax.title("EcoSystem Light distribution")
        axs.axis("off")
        plt.title("EcoSystem Temperture Distribution")
        plt.show()

        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.water_grid,
                            cmap=cm[1])
        fig.colorbar(pcm, ax=axs)
        #ax.title("EcoSystem Water distribution")
        axs.axis("off")
        plt.title("EcoSystem Temperture Distribution")
        plt.show()

        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.temp_grid,
                            cmap=cm[2])
        fig.colorbar(pcm, ax=axs)
        #ax.title("EcoSystem Temperture distribution")
        axs.axis("off")
        plt.title("EcoSystem Temperture Distribution")
        plt.show()

    # MEATHOD: checkCell -----------------------------------------------
    def checkCell(self, x, y):
        """ Description: Gets the cell values at a position from each
                         Graph
            
            Variables: 
                -self: the SimGrid object instance
                
            Output: returns a list of values from each grid
        """
        check = [0, 0, 0]
        check[0] = self.plant_grid[y,x]
        check[1] = self.herbivore_grid[y,x]
        check[2] = self.carnivore_grid[y,x]
        
        return check
    
    # MEATHOD: checkCell -----------------------------------------------
    def randomWalk(self, Fauna):
        """ Description:
            Pass an animal and it will walk within the borders of the grid.
            (Moore's Neighborhood)
        
            Variables: 
            -Fauna.position: current location of fauna
            -moveX: Array of x positions fauna can move
            -moveY: Array of y positions fauna can move
        
            Output: 
                Fauna has changed locations
        """
        
        #Moore Neighborhood walk
        #Directions in x-axis
        moveX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        #Fauna.position[0] current x location
        moveX = moveX + Fauna.position[0]
        
        #Directions in y-axis
        moveY = nu.array([1, 0, -1, 1, -1, 1, 0, -1])
        #Fauna.position[1] current y location
        moveY = moveY + Fauna.position[1]
        
        #Check Borders
        valid = nu.where(nu.logical_not(nu.logical_or( \
        nu.logical_or(moveY >= self.length, moveY < 0),\
        nu.logical_or(moveX >= self.width, moveX < 0))))

        nu.random.shuffle(valid[0])

        #Update grid and animal position
        #X and Y may be flipped for grids
        self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
        self.herbivore_grid[moveX[valid[0][0]], moveY[valid[0][0]]] = 1
        Fauna.position = (moveX[valid[0][0]], moveY[valid[0][0]])
    
    # MEATHOD: checkCell -----------------------------------------------
    def initPlants(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        #For initializing grass
        plantChance = 0.85
        
        #Test every grid space for plant growth
        for i in range(self.length):
            for j in range(self.width):
                #Test for growth
                if nu.random.uniform(0,1) <= plantChance:
                    #Make a grass plant
                    newPlant = fo.Grass()
                    self.plant_grid[i,j] = 1
                    self.plant_list.append(newPlant)
        #Grid and list should now be initialized
    
    # MEATHOD: checkCell -----------------------------------------------
    def initRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        newRab = fa.Rabbit()
        newRab.position = (0,0)
        self.herbivore_list.append(newRab)
        for i in range(1, 4):
            newRab = fa.Rabbit()
            #Spawns 3 around the top left corner
            newRab.position = (i*2,i)
            self.herbivore_list.append(newRab)
            self.herbivore_grid[i*2, i] = 1
            
    def runAFewFrames(self):
        for i in range(5):
            for j in range(len(self.herbivore_list)):
                self.randomWalk(self.herbivore_list[j])

# FUNCTION: FUNC -------------------------------------------------------
def func():
    """ Description:
            
        
        Variables: 
        -var: 
        
        Output: 
    """
    return 2

#=======================================================================   
# PROGRAM SCRIPT ------------------------------------------------------
# Driver code for program

eco = EcoSystem()
eco.displayGrid()
eco.displayFrame()
eco.runAFewFrames()
eco.displayFrame()
eco.runAFewFrames()
eco.displayFrame()
eco.runAFewFrames()
eco.displayFrame()
eco.runAFewFrames()
eco.displayFrame()

#=======================================================================
# END FILE
