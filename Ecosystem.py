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
import random
import math

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

GRID_X = 50                     # var meaning
GRID_Y = 50

NUM_SIMS = 10
NUM_DAYS = 7

# effects lighting
MAX_CLOUDS = 10
CLOUD_CHANCE = 0.6
OVERCAST_CHANCE = 0.2
RAIN_CHANCE = 0.8

# effects water
LAKE_SPREAD = 4
HAS_LAKE = True # bool
POND_SPREAD = 1
NUM_PONDS = 0

# effects temp
WATER_TEMP = -2
LIGHT_TEMP = 2
NATRUAL_TEMP = 10
MAX_TEMP = 32
MIN_TEMP = -32

DISSIPATION_RATE = 0.9
DISSIPATION_SPREAD = 0.8
SCENT_SPREAD = 1

PLANT_CHANCE = 0.9
PLANT_REPOP_CHANCE = 0.1
ENERGY_ABSORB_FACTOR = 1000
WATER_ABSORB_FACTOR = 1000
PLANT_UNITS_TO_EAT = 2

RABBITS_PER_BURROW = 5 # must be less than 9
MAX_RABBITS = 100
NUM_BURROWS = 5

NUM_FOXES = 3

MOVE_CHANCE = 0.5

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
        self.rained = False

        #Grid Size variables
        self.length = 50
        self.width = 50
        
        # These grids track constant values accross the grid
        self.light_grid = nu.ones((self.length, self.width))
        self.water_grid = nu.ones((self.length, self.width))/4
        self.scent_grid = nu.zeros((self.length, self.width))
        self.temp_grid = nu.zeros((self.length+1, self.width))
        self.temp_grid[-1,0] = MIN_TEMP
        self.temp_grid[-1,-1] = MAX_TEMP

        # These grids are booleans(0/1) for when animals are at a location
        self.plant_grid = nu.zeros((self.length, self.width))
        self.herbivore_grid = nu.zeros((self.length, self.width))
        self.burrow_grid = nu.zeros((self.length, self.width))
        self.carnivore_grid = nu.zeros((self.length, self.width))
        
        # These lists hold every individual plant and animal
        self.plant_list = []
        self.herbivore_list = []
        self.carnivore_list = []
        
        #Counting variables
        self.animalsEaten = 0
        self.plantsEaten = 0
        self.plantsDied = 0
        self.carniDied = 0
        self.herbiDied = 0
        
        self.wheatherCheck()
        self.initWater()
        self.updateTemp()
        self.initRabbits()
        self.makePlants(PLANT_CHANCE)
        self.initFoxes()
        self.updateScent()
        
        #self.displayGrid()
        self.displayFrame()
        
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
                elif(self.burrow_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [0.7, 0.7, 0.7]
                elif(self.plant_grid[y,x] == 1):
                    simFrame[shape[0]-y-1, x, :] = [0, 0.4, 0]
                elif(self.water_grid[y,x] >= 1):
                    simFrame[shape[0]-y-1, x, :] = [0, 0.3, 0.7]
                elif(self.water_grid[y,x] >= .75):
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
        pcm = axs.pcolormesh(self.light_grid,
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
        #Use function for when goWater works
        #if Fauna.THIRSTY >= Fauna.water:
        #    self.goWater(Fauna)
        if(nu.random.uniform(0,1) > MOVE_CHANCE):
            #Moore Neighborhood walk
            #Directions in x-axis
            moveX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            #Fauna.position[1] current x location
            moveX = moveX + Fauna.position[1]
            
            #Directions in y-axis
            moveY = nu.array([1, 0, -1, 1, -1, 1, 0, -1])
            #Fauna.position[0] current y location
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
                Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]], self.temp_grid[moveY[valid[0][0]], moveX[valid[0][0]]])
            elif(Fauna.isHerbivore()):
                self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
                self.herbivore_grid[moveY[valid[0][0]], moveX[valid[0][0]]] = 1
                Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]], self.temp_grid[moveY[valid[0][0]], moveX[valid[0][0]]])
        else:
            Fauna.wait()
        
    # METHOD: track ----------------------------------------------------
    def track(self, Fauna):
        #Checks to see if Carnivore should look for food
        if (Fauna.energy > Fauna.hungry):
            return 1
             
        #Looks around itself in a moore neighborhood to find scent
        #Init Moore Neighborhood arrays (same as randomWalk)
        moveX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        moveY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        
        moveX = Fauna.position[1] + moveX
        moveY = Fauna.position[0] + moveY
        
        #Check Borders
        valid = nu.where(nu.logical_not(nu.logical_or(nu.logical_or(moveY >= self.length, moveY < 0),nu.logical_or(moveX >= self.width, moveX < 0))))
        
        scent = nu.zeros(nu.size(valid[0]))
        
        for i in range(len(valid[0])):
            scent[i] = self.scent_grid[moveY[valid[0][i]]][moveX[valid[0][i]]]
            
        strongest_scent = scent.argmax()
        
        duplicates = -1
        for i in range(len(scent)):
            if (scent[strongest_scent] == scent[i]):
                duplicates += 1
            
        indexToUse = strongest_scent
            
        if (duplicates > 0):
            indexToUse = strongest_scent
            currentIndex = 0
            randomNum = random.randint(0, 10)
            while(randomNum > 0):
                if(scent[currentIndex] == scent[strongest_scent]):
                    indexToUse = currentIndex
                    randomNum -= 1
                currentIndex += 1
                if(currentIndex == nu.size(scent)):
                    currentIndex = 0
        
        self.carnivore_grid[Fauna.position[0], Fauna.position[1]] = 0
        self.carnivore_grid[moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]]] = 1
        Fauna.move(moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]], self.temp_grid[moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]]])
        
        return 0
        
    # METHOD: forage ----------------------------------------------------
    def forage(self, Fauna):
        #Checks to see if Herbivore should look for food
        if (Fauna.energy > Fauna.hungry):
            return 1
             
        #Looks around itself in a moore neighborhood to find Flora
        #Init Moore Neighborhood arrays (same as randomWalk)
        moveX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        moveY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        
        moveX = Fauna.position[1] + moveX
        moveY = Fauna.position[0] + moveY
        
        #Check Borders
        valid = nu.where(nu.logical_not(nu.logical_or(nu.logical_or(moveY >= self.length, moveY < 0),nu.logical_or(moveX >= self.width, moveX < 0))))
        
        possibleFood = nu.zeros(nu.size(valid[0]))
        
        for i in range(len(valid[0])):
            possibleFood[i] = self.plant_grid[moveY[valid[0][i]]][moveX[valid[0][i]]]
        
        foundFood = -1
        for i in range(len(possibleFood)):
            if (possibleFood[i] == 1):
                foundFood = i
        
        duplicates = -1
        for i in range(len(possibleFood)):
            if (1 == possibleFood[i]):
                duplicates += 1
        
        if (duplicates == -1):
            return 1
        
        indexToUse = foundFood
        
        if (duplicates > 0):
            currentIndex = indexToUse
            randomNum = random.randint(0, 20)
            while(randomNum > 0):
                if(possibleFood[currentIndex] == 1):
                    indexToUse = currentIndex
                    randomNum -= 1
                currentIndex += 1
                if(currentIndex == nu.size(possibleFood)):
                    currentIndex = 0
        
        self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
        self.herbivore_grid[moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]]] = 1
        Fauna.move(moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]], self.temp_grid[moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]]])
        
        return 0
    
    # METHOD: findWater -------------------------------------------------
    def findWater(self, Fauna):
        if(Fauna.water > Fauna.thirsty):
            return 1
        
        valuesY = []
        valuesX = []
        
        for i in range(self.length):
            for k in range(self.width):
                if (self.water_grid[i][k] >= 1):
                    valuesY.append(i)
                    valuesX.append(k)
                    
        distances  = nu.zeros(len(valuesY))
        
        for i in range(len(valuesY)):
            distances[i] = math.sqrt(math.pow((valuesX[i]-Fauna.position[1]),\
            2) + math.pow((valuesY[i]-Fauna.position[0]), 2))
                    
        closest_water = distances.argmin()
        
        addX = 0
        addY = 0
        
        if(valuesY[closest_water] - Fauna.position[0] > 0):
            addY = 1
        elif(valuesY[closest_water] - Fauna.position[0] < 0):
            addY = -1
        if(valuesX[closest_water] - Fauna.position[1] > 0):
            addX = 1
        elif(valuesX[closest_water] - Fauna.position[1] < 0):
            addX = -1
        
        if(Fauna.isCarnivore()):
            self.carnivore_grid[Fauna.position[0], Fauna.position[1]] = 0
            self.carnivore_grid[Fauna.position[0] + addY, Fauna.position[1] + addX] = 1
            Fauna.move(Fauna.position[0] + addY, Fauna.position[1] + addX, self.temp_grid[Fauna.position[0] + addY, Fauna.position[1] + addX])
        
        elif(Fauna.isHerbivore()):
            self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
            self.herbivore_grid[Fauna.position[0] + addY, Fauna.position[1] + addX] = 1
            Fauna.move(Fauna.position[0] + addY, Fauna.position[1] + addX, self.temp_grid[Fauna.position[0] + addY, Fauna.position[1] + addX])
        
        Fauna.drink(Fauna.drink_amount)
        
        return 0
    
    def goWater(self, Fauna):
        #I do not know how to implement this function (See walk section)
        
        #Init Moore Neighborhood arrays (same as randomWalk)
        moveX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        moveY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
        
        moveX = Fauna.position[1] + moveX
        moveY = Fauna.position[0] + moveY
        
        #Check Borders
        valid = nu.where(nu.logical_not(nu.logical_or( \
        nu.logical_or(moveY >= self.length, moveY < 0),\
        nu.logical_or(moveX >= self.width, moveX < 0))))
        
        
        #Checks nearby spaces within border and drinks if there is water
        for i in range(len(valid[0])):
            if (self.water_grid[moveY[valid[0][i]],moveX[valid[0][i]]] > 0):
                Fauna.drink(Fauna.drink_amount)
                return
        
        #Walk Section: Choose to walk instead
        #I do not know how to implement this part
        return
    
    # METHOD: animalsEat -----------------------------------------------
    def animalsEat(self):
        for i in range(len(self.herbivore_list)):
            #Skip animal if not hungry
            if self.herbivore_list[i].energy > self.herbivore_list[i].hungry:
                continue
                
            else:
                self.eatPlant(self.herbivore_list[i])       
        #iCarn will be every carnivore object in the carnivore_list
        for iCarn in self.carnivore_list:
            if iCarn.hungry > iCarn.energy:
                if self.carnivoreEat(iCarn):
                    continue
                else:
                    #Carnivores do not seem to eat plants when this is used
                    self.eatPlant(iCarn)
                    
    def eatPlant(self, Fauna):
        j = 0
        while(j < len(self.plant_list)):
                #If a plant is found
                if self.plant_list[j].position[0] == Fauna.position[0] and self.plant_list[j].position[1] == Fauna.position[1]:
                    #Eat the max amount if the herbivore is able
                    nutrition = self.plant_list[j].consumed(PLANT_UNITS_TO_EAT)
                    Fauna.eat(nutrition[0])
                    Fauna.drink(nutrition[1])
                    #If the plant dies, remove from grid and list
                    if (not self.plant_list[j].healthCheck()):
                        self.plant_grid[Fauna.position[0], Fauna.position[1]] = 0
                        self.plant_list.remove(self.plant_list[j])
                        self.plantsEaten += 1
                    j = len(self.plant_list)
                else:
                    j += 1
        return
    
    # METHOD: carnivoreEat -----------------------------------------------
    def carnivoreEat(self, Fauna):
        #MoveY and moveX renamed to locY and locX - short for location
        #Boolean flag to let us know if the carnivore has eaten
        eatCheck = False
        
        curY = Fauna.position[0]
        curX = Fauna.position[1]
        
        if self.herbivore_grid[curY, curX] == 1:
            #Search for herbivore object in list
            for iHerb in self.herbivore_list:
                #Location match found
                if iHerb.position[0] == curY and iHerb.position[1] == curX:
                    #Trade energy values
                    nutrition = iHerb.consumed()
                    Fauna.eat(nutrition[0])
                    Fauna.drink(nutrition[1])
                    #Remove herbivore and record its death
                    self.herbivore_list.remove(iHerb)
                    self.animalsEaten += 1
                    eatCheck = True
        
        if(not eatCheck):
            locX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            locY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            
            locX = Fauna.position[1] + locX
            locY = Fauna.position[0] + locY
            
            #Check Borders
            valid = nu.where(nu.logical_not(nu.logical_or( \
            nu.logical_or(locY >= self.length, locY < 0),\
            nu.logical_or(locX >= self.width, locY < 0))))
            
            
            #Check if there is a neighboring herbivore
            for i in range(len(valid)):
                #For readability-currentX and currentY are locations we are checking
                curX = valid[0][i]
                curY = valid[0][i]
                #If a herbivore is spotted
                if self.herbivore_grid[curY, curX] == 1:
                    #Search for herbivore object in list
                    for iHerb in self.herbivore_list:
                        #Location match found
                        if iHerb.position[0] == curY and iHerb.position[1] == curX:
                            #Trade energy values
                            nutrition = iHerb.consumed()
                            Fauna.eat(nutrition[0])
                            Fauna.drink(nutrition[1])
                            #Remove herbivore and record its death
                            self.herbivore_list.remove(iHerb)
                            self.animalsEaten += 1
                            eatCheck = True
            #return a true or false depending on action - can do something about it
            #later
             
        return eatCheck
    
    def plantsAbsorb(self):
        for iPlant in self.plant_list:
            lighting = self.light_grid[iPlant.position[0], iPlant.position[1]]
            iPlant.photosynth(lighting * ENERGY_ABSORB_FACTOR)
            water = self.water_grid[iPlant.position[0], iPlant.position[1]]
            iPlant.drink(water * WATER_ABSORB_FACTOR)
            
    def checkPlantGrowth(self):
        for iPlant in self.plant_list:
            iPlant.growth()
    
    def checkStarved(self):
        """Removes animals and plants that are no longer alive
        """
        for iHerb in self.herbivore_list:
            if not iHerb.healthCheck():
                self.herbivore_grid[iHerb.position[0], iHerb.position[1]] = 0
                self.herbivore_list.remove(iHerb)
                self.herbiDied += 1
            
        for iCarn in self.carnivore_list:
            if not iCarn.healthCheck():
                self.carnivore_grid[iCarn.position[0], iCarn.position[1]] = 0
                self.carnivore_list.remove(iCarn)
                self.carniDied += 1
                
        for iPlant in self.plant_list:
            if not iPlant.healthCheck():
                self.plant_grid[iPlant.position[0], iPlant.position[1]] = 0
                self.plant_list.remove(iPlant)
                self.plantsDied += 1
        return
    
    def updateScent(self):
        spreadScent = nu.zeros((self.length + (SCENT_SPREAD * 2), self.width + (SCENT_SPREAD * 2)))
        spreadScent[SCENT_SPREAD:-(SCENT_SPREAD), SCENT_SPREAD:-(SCENT_SPREAD)] = self.scent_grid
        for y in range(SCENT_SPREAD, self.length + SCENT_SPREAD):
            for x in range(SCENT_SPREAD, self.width + SCENT_SPREAD):        
                spreadScent[y-SCENT_SPREAD:y+SCENT_SPREAD, x-SCENT_SPREAD] = spreadScent[y,x] * DISSIPATION_SPREAD
                spreadScent[y-SCENT_SPREAD:y+SCENT_SPREAD, x+SCENT_SPREAD] = spreadScent[y,x] * DISSIPATION_SPREAD
                spreadScent[y-SCENT_SPREAD, x] = spreadScent[y,x] * DISSIPATION_SPREAD
                spreadScent[y+SCENT_SPREAD, x] = spreadScent[y,x] * DISSIPATION_SPREAD
                
        herb_scent = nu.fmax(self.herbivore_grid, self.scent_grid * DISSIPATION_RATE, spreadScent[SCENT_SPREAD:-(SCENT_SPREAD), SCENT_SPREAD:-(SCENT_SPREAD)])
        carn_scent = nu.fmax(self.carnivore_grid, self.scent_grid * DISSIPATION_RATE * -1, spreadScent[SCENT_SPREAD:-(SCENT_SPREAD), SCENT_SPREAD:-(SCENT_SPREAD)]*-1)
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
        
        x = [5, 10, 15, 35, 40, 45]
        y = [5, 10, 15, 35, 40, 45]
        nu.random.shuffle(x)
        nu.random.shuffle(y)
        
        ponds = NUM_PONDS
        
        if(ponds > len(x)):
            ponds = len(x)  # ensures that we don't try to make more
                            # than we have available positions for
                                
        for i in range(ponds):
            x1 = int(nu.random.uniform(-2,0)) + x[i]
            x2 = int(nu.random.uniform(0,2)) + x[i]
            y1 = int(nu.random.uniform(-2,0)) + y[i]
            y2 = int(nu.random.uniform(0,2)) + y[i]
            self.makeWaterBody(x1, y1, x2, y2, POND_SPREAD)
            
        if(HAS_LAKE):
            self.makeWaterBody(24, 24, 26, 26, LAKE_SPREAD)
        
    def makeWaterBody(self, x1, y1, x2, y2, spread):
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
            self.water_grid[y-spread*3:y+spread*3, x-spread*3:x+spread*3] = 0.5  
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
       
        x = ax
        y = ay
        while (x < bx or y < by):         
            self.water_grid[y-spread*2:y+spread*2, x-spread*2:x+spread*2] = 0.75
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
            
        x = ax
        y = ay
        while (x < bx or y < by):
            self.water_grid[y-spread:y+spread, x-spread:x+spread] = 1
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
    
    # MEATHOD: checkCell -----------------------------------------------
    def wheatherCheck(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        if(self.rained):
            self.water_grid -= 0.2
            self.rained = False
        elif(nu.random.uniform(0,1) < OVERCAST_CHANCE):
            self.light_grid *= 0.3
            if(nu.random.uniform(0,1) < RAIN_CHANCE):
                self.water_grid += 0.2
                self.rained = True
        else:
            self.light_grid = nu.ones((self.length, self.width))
            for i in range(MAX_CLOUDS):
                if(nu.random.uniform(0,1) < CLOUD_CHANCE):
                    self.makeCloud()
    
    # MEATHOD: checkCell -----------------------------------------------
    def makeCloud(self):
        x = int(nu.random.uniform(0,1) * 50)
        y = int(nu.random.uniform(0,1) * 50)
        
        thickness = nu.random.uniform(0.3,0.7)
        spreadX = int(nu.random.uniform(3,15))
        spreadY = int(nu.random.uniform(3,15))
        
        self.light_grid[y-spreadY:y+spreadY, x-spreadX:x+spreadX] *= 1-thickness
        
    # MEATHOD: checkCell -----------------------------------------------
    def updateTemp(self):
        """ Description:
            
            Populates the plant list by determining if a plant grows in an area
            using a random number.
        
            Variables: 
            -plantChance: Chance a plant will grow in a grid space.
        
            Output: plant_list and plant_grid is populated with Grass objects.
        """
        self.temp_grid[:-1,:] = NATRUAL_TEMP
        self.temp_grid[:-1,:] += self.water_grid * WATER_TEMP
        self.temp_grid[:-1,:] += self.light_grid * LIGHT_TEMP
    
    # MEATHOD: checkCell -----------------------------------------------
    def makePlants(self, chance):
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
                if nu.random.uniform(0,1) <= chance:
                    if(self.water_grid[y,x] < 0.75 and self.plant_grid[y,x] < 1 and self.burrow_grid[y,x] < 1):
                        #Make a grass plant
                        newPlant = fo.Grass(y,x)
                        self.plant_grid[y,x] = 1
                        self.plant_list.append(newPlant)
        #Grid and list should now be initialized
        
    # MEATHOD: checkCell -----------------------------------------------
    def initRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        
        i = 0
        while(i < NUM_BURROWS):
            x = int(nu.random.uniform(2,self.width - 2))
            y = int(nu.random.uniform(2,self.length - 2))
            if(self.water_grid[y,x] < 0.75 and self.burrow_grid[y,x] < 1):
                self.burrow_grid[y,x] = 1
                i += 1
            
        self.spawnRabbits()
    
    # MEATHOD: checkCell -----------------------------------------------
    def spawnRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        
        for y in range(self.length):
            for x in range(self.width):
                if(self.burrow_grid[y,x] == 1):
                    placeX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
                    placeY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            
                    nu.random.shuffle(placeX)
                    nu.random.shuffle(placeY)
                    
                    for j in range(RABBITS_PER_BURROW):
                        if(len(self.herbivore_list) >= MAX_RABBITS):
                            return
                        
                        locX = x + placeX[j]
                        locY = y + placeY[j]
                        
                        newRab = fa.Rabbit(locY,locX)
                        #Spawns around the burrow
                        self.herbivore_list.append(newRab)
                        self.herbivore_grid[locY, locX] = 1
            
    def initFoxes(self):
        #This fox spawn is hardcoded so we could keep them away from vulnerable
        #animals
        
        for i in range(NUM_FOXES):
            x = int(nu.random.uniform(0,self.width))
            y = int(nu.random.uniform(0,self.length))
            newFox = fa.Fox(y,x)
            self.carnivore_list.append(newFox)
            self.carnivore_grid[y, x] = 1
     
    # MEATHOD: runAFewFrames -------------------------------------------
    def runADay(self):
        for i in range(24):
            for j in range(len(self.herbivore_list)):
                if(self.findWater(self.herbivore_list[j])):
                    if(self.forage(self.herbivore_list[j])):
                        self.randomWalk(self.herbivore_list[j])
            for j in range(len(self.carnivore_list)):
                for k in range(fa.EXTRA_FOX_STEPS):
                    if(self.findWater(self.carnivore_list[j])):
                        if(self.track(self.carnivore_list[j])):
                            self.randomWalk(self.carnivore_list[j])
            self.animalsEat()
            self.updateScent()
            self.plantsAbsorb()
        
        # do at the end of each day
        self.wheatherCheck()
        self.updateTemp()
        self.checkPlantGrowth()
        self.checkStarved()
        
    # MEATHOD: runAFewFrames -------------------------------------------
    def runAWeek(self):
        for i in range(7):
            self.runADay()
        self.makePlants(PLANT_REPOP_CHANCE)
    
    def runAMonth(self):
        for i in range(4):
            self.runAWeek()
        self.spawnRabbits()
        
#=======================================================================   
# Analysis Functions --------------------------------------------------
def anRabToPlant(perBurrow, numBurrows):
    #Parameters passed
    global RABBITS_PER_BURROW
    RABBITS_PER_BURROW = perBurrow # must be less than 9
    global NUM_BURROWS
    NUM_BURROWS = numBurrows
    
    beginningPlants = []
    endPlants = []
    
    print("Rabbits per Burrow: ", perBurrow)
    print("Burrows:", numBurrows)
    print("TotalRabbits:", perBurrow * numBurrows)
    
    for j in range(NUM_SIMS):
        eco = EcoSystem()           #Initialize Ecosystem
        beginningPlants.append(len(eco.plant_list))
        for i in range(NUM_DAYS):
            eco.runADay()
        endPlants.append(len(eco.plant_list))
        
    avgBeginning = sum(beginningPlants) / len(beginningPlants)
    avgEnd = sum(endPlants) / len(endPlants)
    print("# Simulations:", NUM_SIMS)
    print("Average plants at beginning:", avgBeginning)
    print("Average plants at end:", avgEnd)
    print("Average plant difference:", avgBeginning - avgEnd, "\n")
    
def anLakeToRab(spread):
    global LAKE_SPREAD
    LAKE_SPREAD = spread
    print("Lake Spread:", spread)
    endRabbits = []
    for j in range(NUM_SIMS):
        eco = EcoSystem()
        for i in range(NUM_DAYS):
            eco.runADay()  
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", NUM_SIMS)
    print("Average rabbits at end:", avgEnd)
    
def anDissipationtoRab(dis):
    global DISSIPATION_RATE
    DISSIPATION_RATE = dis
    
    print("Dissipation Rate:", dis)
    endRabbits = []
    
    for j in range(NUM_SIMS):
        eco = EcoSystem()
        for i in range(NUM_DAYS):
            eco.runADay()  
        endRabbits.append(len(eco.herbivore_list))
    
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", NUM_SIMS)
    print("Average rabbits at end:", avgEnd, "\n")
    
def anFoxToRab(fox):
    global NUM_FOXES
    NUM_FOXES = fox
    
    print("Foxes:", fox)
    endRabbits = []
    dayExtinct = []
    
    lastDay = 0
    for j in range(NUM_SIMS):
        lastDay = 10
        eco = EcoSystem()
        for i in range(NUM_DAYS):
            eco.runADay()  
            #Check if all rabbits are dead
            if len(eco.herbivore_list) == 0:
                if i < lastDay:
                    lastDay = i
        dayExtinct.append(lastDay)
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    avgDay = sum(dayExtinct) / len(dayExtinct)
    print("# Simulations:", NUM_SIMS)
    
    print("Average rabbits at end:", avgEnd)
    print("Average day eliminated:", avgDay, "\n")

#=======================================================================   
# PROGRAM SCRIPT ------------------------------------------------------
# Driver code for program

eco = EcoSystem()

initPlants = len(eco.plant_list)
initRabs = len(eco.herbivore_list)
initFoxes = len(eco.carnivore_list)

for i in range(NUM_DAYS):
    eco.frame += 1
    eco.runADay()
    eco.displayFrame()
    #eco.displayGrid()

print("--Simulation Config--")
print("")
print("Grid Length:", eco.length)
print("Grid Width:", eco.width)
print("Number of Days:", NUM_DAYS)
print("Time Units Per Day:", 24)
print("Total Time Units:", 24 * NUM_DAYS)
# todo add in some values from eco for displaying
print("")
print("--Simulation Results--")
print("")
print("Natrual Deaths:")
print("   -Plants:", eco.plantsDied)
print("   -Herbivores:", eco.herbiDied)
print("   -Carnivores:", eco.carniDied)
print("")
print("Eaten:")
print("   -Plants:", eco.plantsEaten)
print("   -Animals:", eco.animalsEaten)
print("")

#=======================================================================
# END FILE
