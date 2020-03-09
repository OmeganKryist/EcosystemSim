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

WATER_SPREAD = 4
WATER_TEMP = -4
LIGHT_TEMP = 2

DISSIPATION_RATE = 0.8

PLANT_CHANCE = 0.9
NUM_RABBITS = 5
NUM_BURROWS = 3
NUM_FOXES = 1


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
        self.frame = 0

        #Grid Size variables
        self.length = 50
        self.width = 50
        
        # These grids track constant values accross the grid
        self.light_grid = nu.ones((self.length, self.width))
        self.water_grid = nu.ones((self.length, self.width))/4
        self.temp_grid = nu.zeros((self.length+1, self.width))
        self.scent_grid = nu.zeros((self.length, self.width))

        # These grids are booleans(0/1) for when animals are at a location
        self.plant_grid = nu.zeros((self.length, self.width))
        self.herbivore_grid = nu.zeros((self.length, self.width))
        self.carnivore_grid = nu.zeros((self.length, self.width))
        
        # These lists hold every individual plant and animal
        self.plant_list = []
        self.herbivore_list = []
        self.carnivore_list = []
        
        self.initWater()
        self.updateTemp()
        self.initPlants()
        self.initRabbits()
        self.initFoxes()
        
    # MEATHOD: displayGrid ---------------------------------------------
    def displayFrame(self):
        """ Description: displays a frame from the simulation
            
            Variables: 
                -self: the SimGrid object instance
        """
        # get boarder values of rgb grid
        simFrame = nu.full((self.length, self.width, 3), [0.2, 0.2, 0])
        
        # get values of rgb grid
        shape = nu.shape(simFrame)
        
        for y in range(shape[0]):
            for x in range(shape[1]):
                if(self.carnivore_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [1, 0.6, 0]
                elif(self.herbivore_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [1, 1, 1] 
                elif(self.plant_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [0, 0.4, 0]
                elif(self.water_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [0, 0.3, 0.7]
                elif(self.water_grid[y,x] == .75):
                    simFrame[shape[0]-y-1, x, :] = [0.5, 0.7, 0.9]

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
        
        cm = ['YlOrBr_r', 'Blues', 'coolwarm', 'PRGn']
        
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.plant_grid,
                            cmap=cm[0])
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Light Distribution")
        plt.show()

        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.water_grid,
                            cmap=cm[1])
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Water Distribution")
        plt.show()

        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.temp_grid,
                            cmap=cm[2])
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Temperture Distribution")
        plt.show()
        
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.scent_grid,
                            cmap=cm[3])
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Scent Distribution")
        plt.show()

    # MEATHOD: checkCell -----------------------------------------------
    def checkCell(self, x, y):
        """ Description: Gets the cell values at a position from each
                         Graph
            
            Variables: 
                -self: the SimGrid object instance
                
            Output: returns a list of values from each grid
        """
        check = [0, 0, 0, 0, 0, 0]
        check[0] = self.light_grid[y,x]
        check[1] = self.water_grid[y,x]
        check[2] = self.temp_grid[y,x]
        check[3] = self.plant_grid[y,x]
        check[4] = self.herbivore_grid[y,x]
        check[5] = self.carnivore_grid[y,x]
        
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
        moveX = moveX + Fauna.position[1]
        
        #Directions in y-axis
        moveY = nu.array([1, 0, -1, 1, -1, 1, 0, -1])
        #Fauna.position[1] current y location
        moveY = moveY + Fauna.position[0]
        
        #Check Borders
        valid = nu.where(nu.logical_not(nu.logical_or( \
        nu.logical_or(moveY >= self.length, moveY < 0),\
        nu.logical_or(moveX >= self.width, moveX < 0))))

        nu.random.shuffle(valid[0])

        #Update grid and animal position
        #X and Y may be flipped for grids
        if(Fauna.isCarnivore()):
            self.carnivore_grid[Fauna.position[0], Fauna.position[1]] = 0
            self.carnivore_grid[moveY[valid[0][0]], moveX[valid[0][0]]] = 1
            Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]])
        elif(Fauna.isHerbivore()):
            self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
            self.herbivore_grid[moveY[valid[0][0]], moveX[valid[0][0]]] = 1
            Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]])
        
    # MEATHOD: checkCell -----------------------------------------------
    def animalsEat(self):
        for i in range(len(self.herbivore_list)):
            j = 0
            while(j < len(self.plant_list)):
                #If a plant is found
                if self.plant_list[j].position[0] == self.herbivore_list[i].position[0] and self.plant_list[j].position[1] == self.herbivore_list[i].position[1]:
                    #Eat the max amount if the herbivore is able
                    self.herbivore_list[i].eat(self.plant_list[j].consumed(self.herbivore_list[i].eatAmt))
                    #If the plant dies, remove from grid and list
                    if (not self.plant_list[j].healthCheck()):
                        self.plant_grid[self.herbivore_list[i].position[0], self.herbivore_list[i].position[1]] == 0
                        self.plant_list.remove(self.plant_list[j])
                    j = len(self.plant_list)
                else:
                    j += 1
                        
    def updateScent(self):
        herb_scent = nu.fmax(self.herbivore_grid, self.scent_grid * DISSIPATION_RATE)
        carn_scent = nu.fmax(self.carnivore_grid, self.scent_grid * DISSIPATION_RATE * -1)
        self.scent_grid = herb_scent - carn_scent
                   
    # MEATHOD: checkCell -----------------------------------------------
    def initWater(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        self.makeWaterBody(20,10,30,30)
        
    def makeWaterBody(self, x1, y1, x2, y2):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        ax = min(x1,x2)
        bx = max(x1,x2)
        ay = min(y1,y2)
        by = max(y1,y2)
        
        x = ax
        y = ay
        while (x < bx or y < by):
            self.water_grid[y-WATER_SPREAD*3:y+WATER_SPREAD*3, x-WATER_SPREAD*3:x+WATER_SPREAD*3] = 0.5  
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
       
        x = ax
        y = ay
        while (x < bx or y < by):         
            self.water_grid[y-WATER_SPREAD*2:y+WATER_SPREAD*2, x-WATER_SPREAD*2:x+WATER_SPREAD*2] = 0.75
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
            
        x = ax
        y = ay
        while (x < bx or y < by):
            self.water_grid[y-WATER_SPREAD:y+WATER_SPREAD, x-WATER_SPREAD:x+WATER_SPREAD] = 1
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
                
    # MEATHOD: checkCell -----------------------------------------------
    def updateTemp(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        self.temp_grid[:-1,:] = self.water_grid * WATER_TEMP
        self.temp_grid[:-1,:] += self.light_grid * LIGHT_TEMP
        self.temp_grid[-1,0] = -5
        self.temp_grid[-1,-1] = 5
    
    # MEATHOD: checkCell -----------------------------------------------
    def initPlants(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        
        #Test every grid space for plant growth
        for y in range(self.length):
            for x in range(self.width):
                #Test for growth
                if nu.random.uniform(0,1) <= PLANT_CHANCE:
                    if(self.water_grid[y,x] < 0.75):
                        #Make a grass plant
                        newPlant = fo.Grass(y,x)
                        self.plant_grid[y,x] = 1
                        self.plant_list.append(newPlant)
        #Grid and list should now be initialized
    
    # MEATHOD: checkCell -----------------------------------------------
    def initRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        
        for i in range(NUM_BURROWS):
            x = 3 * i
            y = 5 * i
            
        self.spawnRabbits()
    
    # MEATHOD: checkCell -----------------------------------------------
    def spawnRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        for i in range(NUM_RABBITS):
            x = i * 2
            y = i
            newRab = fa.Rabbit(y,x)
            #Spawns 3 around the top left corner
            self.herbivore_list.append(newRab)
            self.herbivore_grid[y, x] = 1
            
    def initFoxes(self):
        #This fox spawn is hardcoded so we could keep them away from vulnerable
        #animals
        
        for i in range(NUM_FOXES):
            x = 35
            y = 30
            newFox = fa.Fox(y,x)
            self.carnivore_list.append(newFox)
            self.carnivore_grid[y, x] = 1
     
    # MEATHOD: runAFewFrames -------------------------------------------
    def runAFewFrames(self):
        for i in range(5):
            for j in range(len(self.herbivore_list)):
                self.randomWalk(self.herbivore_list[j])
            for j in range(len(self.carnivore_list)):
                self.randomWalk(self.carnivore_list[j])
            self.animalsEat()
            self.updateScent()
        
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

value = len(eco.plant_list)

for i in range(10):
    eco.frame += 1
    eco.runAFewFrames()
    #eco.animalsEat()
    eco.displayFrame()

print("# plants died:")
print(value - len(eco.plant_list))

eco.displayGrid()

#=======================================================================
# END FILE

