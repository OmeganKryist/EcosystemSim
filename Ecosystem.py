# START FILE
#==============================================================================
# GENERAL DOCUMENTATION _______________________________________________________
""" 
"""

# ADDITIONAL DOCUMENTATION ____________________________________________________

# Modification History:
# - 3 Mar 2020: File Created

# Notes:
# - Written for Python 3.7
# - To test simply run the file in the canopy distribution of python
#  or through some other IDE like visual studio or spyder
# - Documentation style inspired by CSS 458 professor Johnny Lin

#==============================================================================
# PROGRAM IMPORTS _____________________________________________________________
import Variables as const
import Fauna as fa
import Flora as fo
import numpy as nu
import matplotlib.pyplot as plt
import random
import math

#==============================================================================
# CLASS: Ecosystem ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EcoSystem:
    """ Description:
    
        Variables: 
        -var: 
    
        Methods: 
    """
    
    
    # MEATHOD: INIT -----------------------------------------------------------
    def __init__(self):
        """ Description: Class constructor
            
    
            Variables: 
            -var: 
    
            Output: 
        """
        self.frame = 0
        self.iterations = 0
        self.rained = False

        #Grid Size variables
        self.length = const.GRID_Y
        self.width = const.GRID_X
        
        # These grids track constant values accross the grid
        self.light_grid = nu.ones((self.length, self.width))
        self.water_grid = nu.ones((self.length, self.width))/4
        self.scent_grid = nu.zeros((self.length, self.width))
        self.temp_grid = nu.zeros((self.length+1, self.width))
        self.temp_grid[-1,0] = const.MIN_TEMP
        self.temp_grid[-1,-1] = const.MAX_TEMP

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
        self.plantsEaten = 0
        self.plantsDied = 0
        self.carniDied = 0
        self.herbiDied = 0
        self.animalsDeath = [0, 0, 0, 0, 0]
        self.timesDrunk = 0
        self.timesRained = 0
        self.carniMove = [0, 0, 0, 0]
        self.herbiMove = [0, 0, 0, 0]
        
        # initalization functions
        self.wheatherCheck()
        self.initWater()
        self.updateTemp()
        self.initRabbits()
        self.makePlants(const.PLANT_CHANCE)
        self.initFoxes()
        self.updateScent()
        
        # inital display
        self.displayGrids()
        
    # MEATHOD: displayFrame ---------------------------------------------------
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
        fig, axs = plt.subplots(1, 1)
        plt.title("EcoSystem Simulation Frame: " + str(self.frame))
        axs.axis("off")
        axs.imshow(simFrame)
        plt.pause(0.5)

    # MEATHOD: displayScent ---------------------------------------------------
    def displayScent(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        
        cm = 'PRGn'
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.scent_grid,
                            cmap=cm)
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Scent Distribution")
        plt.show()
        
    # MEATHOD: displayTemp ----------------------------------------------------
    def displayTemp(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        
        cm = 'coolwarm'
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.temp_grid,
                            cmap=cm)
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Temperture Distribution")
        plt.show()
        
    # MEATHOD: displayLight ---------------------------------------------------
    def displayLight(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        
        cm = 'YlOrBr_r'
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.light_grid,
                            cmap=cm)
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Light Distribution")
        plt.show()

    
    # MEATHOD: displayWater ---------------------------------------------------
    def displayWater(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        
        cm = 'Blues'
        fig, axs = plt.subplots(1, 1)
        pcm = axs.pcolormesh(self.water_grid,
                            cmap=cm)
        fig.colorbar(pcm, ax=axs)
        axs.axis("off")
        plt.title("EcoSystem Water Distribution")
        plt.show()
    
    # MEATHOD: displayGrids ---------------------------------------------------
    def displayGrids(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        self.displayLight()
        self.displayWater()
        self.displayTemp()
        self.displayScent()
        self.displayFrame()
        
    
    # MEATHOD: displayResults ------------------------------------------------- 
    def displayResults(self):
        """ Description: displays constant grid color maps
            
            Variables: 
                -self: the SimGrid object instance
        """
        print("")
        print("--Simulation Config--")
        print("")
        print("Grid Length:", self.length)
        print("Grid Width:", self.width)
        print("Itterations:", self.iterations)
        print("")
        print("--Simulation Results--")
        print("")
        print("Plant Deaths:")
        print("   -Decay:", self.plantsDied)
        print("   -Eaten:", self.plantsEaten)
        print("")
        print("Animal Deaths:")
        print("   -Starved:", self.animalsDeath[0])
        print("   -Desiccated:", self.animalsDeath[1])
        print("   -Frozen:", self.animalsDeath[2])
        print("   -Boiled:", self.animalsDeath[3])
        print("   -Eaten:", self.animalsDeath[4])
        print("   -Herbivores:", self.herbiDied)
        print("   -Carnivores:", self.carniDied)
        print("")
        print("Water:")
        print("   -Times Drunk:", self.timesDrunk)
        print("   -Times Rained:", self.timesRained)
        print("")
        print("Herbivore Movement:")
        print("   -Times Looking For Water:", self.herbiMove[2])
        print("   -Times Looking For Energy:", self.herbiMove[1])
        print("   -Times Randomly walked:", self.herbiMove[0])
        print("   -Times Waited:", self.herbiMove[3])
        print("")
        print("Carnivore Movement:")
        print("   -Times Looking For Water:", self.carniMove[2])
        print("   -Times Looking For Energy:", self.carniMove[1])
        print("   -Times Randomly walked:", self.carniMove[0])
        print("   -Times Waited:", self.carniMove[3])
        print("")
    
    # MEATHOD: randomWalk -----------------------------------------------------
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
        if(nu.random.uniform(0,1) > const.MOVE_CHANCE):
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
                Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]],\
                           self.temp_grid[moveY[valid[0][0]],\
                                          moveX[valid[0][0]]])
                self.carniMove[0] += 1
            elif(Fauna.isHerbivore()):
                self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
                self.herbivore_grid[moveY[valid[0][0]], moveX[valid[0][0]]] = 1
                Fauna.move(moveY[valid[0][0]], moveX[valid[0][0]],\
                           self.temp_grid[moveY[valid[0][0]],\
                                          moveX[valid[0][0]]])
                self.herbiMove[0] += 1
        else:
            Fauna.wait()
            if(Fauna.isCarnivore()):
                self.carniMove[3]
            elif(Fauna.isHerbivore()):
                self.herbiMove[3] += 1
        
    # METHOD: track -----------------------------------------------------------
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
        valid = nu.where(nu.logical_not(nu.logical_or(nu.logical_or(\
                moveY >= self.length, moveY < 0),\
                nu.logical_or(moveX >= self.width, moveX < 0))))
        
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
        self.carnivore_grid[moveY[valid[0][indexToUse]],\
                            moveX[valid[0][indexToUse]]] = 1
        Fauna.move(moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]],\
                   self.temp_grid[moveY[valid[0][indexToUse]],\
                                  moveX[valid[0][indexToUse]]])
        self.carniMove[1] += 1
        return 0
        
    # METHOD: forage ----------------------------------------------------------
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
        valid = nu.where(nu.logical_not(nu.logical_or(nu.logical_or(\
                moveY >= self.length, moveY < 0),\
                nu.logical_or(moveX >= self.width, moveX < 0))))
        
        possibleFood = nu.zeros(nu.size(valid[0]))
        
        for i in range(len(valid[0])):
            possibleFood[i] = self.plant_grid[moveY[valid[0][i]]]\
                                                [moveX[valid[0][i]]]
        
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
        self.herbivore_grid[moveY[valid[0][indexToUse]],\
                            moveX[valid[0][indexToUse]]] = 1
        Fauna.move(moveY[valid[0][indexToUse]], moveX[valid[0][indexToUse]],\
                   self.temp_grid[moveY[valid[0][indexToUse]],\
                                  moveX[valid[0][indexToUse]]])
        self.herbiMove[1] += 1
        return 0
    
    # METHOD: findWater -------------------------------------------------------
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
            self.carnivore_grid[Fauna.position[0] + addY,\
                                Fauna.position[1] + addX] = 1
            Fauna.move(Fauna.position[0] + addY, Fauna.position[1] + addX,\
                       self.temp_grid[Fauna.position[0] + addY,\
                                      Fauna.position[1] + addX])
            self.carniMove[2] += 1
        elif(Fauna.isHerbivore()):
            self.herbivore_grid[Fauna.position[0], Fauna.position[1]] = 0
            self.herbivore_grid[Fauna.position[0] + addY,\
                                Fauna.position[1] + addX] = 1
            Fauna.move(Fauna.position[0] + addY, Fauna.position[1] + addX,\
                       self.temp_grid[Fauna.position[0] + addY,\
                                      Fauna.position[1] + addX])
            self.herbiMove[2] += 1
        
        Fauna.drink(Fauna.drink_amount)
        self.timesDrink += 1
        return 0
    
    # METHOD: animalsEat ------------------------------------------------------
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
             
    # MEATHOD: eatPlant -------------------------------------------------------
    def eatPlant(self, Fauna):
        j = 0
        while(j < len(self.plant_list)):
                #If a plant is found
                if self.plant_list[j].position[0] == Fauna.position[0] and\
                self.plant_list[j].position[1] == Fauna.position[1]:
                    #Eat the max amount if the herbivore is able
                    nutrition = \
                        self.plant_list[j].consumed(const.PLANT_UNITS_TO_EAT)
                    Fauna.eat(nutrition[0])
                    Fauna.drink(nutrition[1])
                    #If the plant dies, remove from grid and list
                    if (not self.plant_list[j].healthCheck()):
                        self.plant_grid[Fauna.position[0],\
                                        Fauna.position[1]] = 0
                        self.plant_list.remove(self.plant_list[j])
                        self.plantsEaten += 1
                    j = len(self.plant_list)
                else:
                    j += 1
        return
    
    # METHOD: carnivoreEat ----------------------------------------------------
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
                    self.animalsDeath[4] += 1
                    eatCheck = True
        
        if(not eatCheck):
            locX = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            locY = nu.array([1, 1, 1, 0, 0, -1, -1, -1])
            
            locX = Fauna.position[1] + locX
            locY = Fauna.position[0] + locY
            
            # Check Borders
            valid = nu.where(nu.logical_not(nu.logical_or(\
            nu.logical_or(locY >= self.length, locY < 0),\
            nu.logical_or(locX >= self.width, locY < 0))))
            
            
            # Check if there is a neighboring herbivore
            for i in range(len(valid)):
                # For readability-currentX and currentY are locations we 
                # are checking
                curX = valid[0][i]
                curY = valid[0][i]
                #If a herbivore is spotted
                if self.herbivore_grid[curY, curX] == 1:
                    #Search for herbivore object in list
                    for iHerb in self.herbivore_list:
                        #Location match found
                        if iHerb.position[0] == curY and\
                        iHerb.position[1] == curX:
                            #Trade energy values
                            nutrition = iHerb.consumed()
                            Fauna.eat(nutrition[0])
                            Fauna.drink(nutrition[1])
                            #Remove herbivore and record its death
                            self.herbivore_list.remove(iHerb)
                            self.animalsDeath[4] += 1
                            eatCheck = True
            #return a true or false depending on action - can do something 
            # about it later
        return eatCheck
    
    # MEATHOD: plantsAbsorb ---------------------------------------------------
    def plantsAbsorb(self):
        for iPlant in self.plant_list:
            lighting = self.light_grid[iPlant.position[0], iPlant.position[1]]
            iPlant.photosynth(lighting * const.ENERGY_ABSORB_FACTOR)
            water = self.water_grid[iPlant.position[0], iPlant.position[1]]
            iPlant.drink(water * const.WATER_ABSORB_FACTOR)
    
    # MEATHOD: checkPlantGrowth -----------------------------------------------      
    def checkPlantGrowth(self):
        for iPlant in self.plant_list:
            iPlant.growth()
    
    # MEATHOD: checkStarved ---------------------------------------------------
    def checkStarved(self):
        """ Removes animals and plants that are no longer alive
        """
        for iHerb in self.herbivore_list:
            checks = iHerb.healthCheck()
            if not checks[0]:
                self.herbivore_grid[iHerb.position[0], iHerb.position[1]] = 0
                self.herbivore_list.remove(iHerb)
                self.herbiDied += 1
                if(not (checks[1] == -1)):
                    self.animalsDeath[checks[1]] += 1 
            
        for iCarn in self.carnivore_list:
            checks = iCarn.healthCheck()
            if not checks[0]:
                self.carnivore_grid[iCarn.position[0], iCarn.position[1]] = 0
                self.carnivore_list.remove(iCarn)
                self.carniDied += 1
                if(not (checks[1] == -1)):
                    self.animalsDeath[checks[1]] += 1 
                
        for iPlant in self.plant_list:
            if not iPlant.healthCheck():
                self.plant_grid[iPlant.position[0], iPlant.position[1]] = 0
                self.plant_list.remove(iPlant)
                self.plantsDied += 1
        return
    
    # MEATHOD: updateScent ----------------------------------------------------
    def updateScent(self):
        spreadScent = nu.zeros((self.length + (const.SCENT_SPREAD * 2),\
                                self.width + (const.SCENT_SPREAD * 2)))
        spreadScent[const.SCENT_SPREAD:-(const.SCENT_SPREAD),\
                    const.SCENT_SPREAD:-(const.SCENT_SPREAD)] = self.scent_grid
        for y in range(const.SCENT_SPREAD, self.length + const.SCENT_SPREAD):
            for x in range(const.SCENT_SPREAD,\
                           self.width + const.SCENT_SPREAD):        
                spreadScent[y-const.SCENT_SPREAD:y+const.SCENT_SPREAD,\
                            x-const.SCENT_SPREAD] =\
                            spreadScent[y,x] * const.DISSIPATION_SPREAD
                spreadScent[y-const.SCENT_SPREAD:y+const.SCENT_SPREAD,\
                            x+const.SCENT_SPREAD] =\
                            spreadScent[y,x] * const.DISSIPATION_SPREAD
                spreadScent[y-const.SCENT_SPREAD, x] =\
                spreadScent[y,x] * const.DISSIPATION_SPREAD
                spreadScent[y+const.SCENT_SPREAD, x] =\
                spreadScent[y,x] * const.DISSIPATION_SPREAD
                
        herb_scent = nu.fmax(self.herbivore_grid,\
                             self.scent_grid * const.DISSIPATION_RATE,\
                             spreadScent[const.SCENT_SPREAD:\
                                         -(const.SCENT_SPREAD),\
                                         const.SCENT_SPREAD:\
                                         -(const.SCENT_SPREAD)])
        carn_scent = nu.fmax(self.carnivore_grid,\
                             self.scent_grid * const.DISSIPATION_RATE * -1,\
                             spreadScent[const.SCENT_SPREAD:\
                                         -(const.SCENT_SPREAD),\
                                         const.SCENT_SPREAD:\
                                         -(const.SCENT_SPREAD)]*-1)
        self.scent_grid = herb_scent - carn_scent
                   
    # MEATHOD: initWater ------------------------------------------------------
    def initWater(self):
        x = [5, 10, 15, 35, 40, 45]
        y = [5, 10, 15, 35, 40, 45]
        nu.random.shuffle(x)
        nu.random.shuffle(y)
        
        ponds = const.NUM_PONDS
        
        if(ponds > len(x)):
            ponds = len(x)  # ensures that we don't try to make more
                            # than we have available positions for
                                
        for i in range(ponds):
            x1 = int(nu.random.uniform(-2,0)) + x[i]
            x2 = int(nu.random.uniform(0,2)) + x[i]
            y1 = int(nu.random.uniform(-2,0)) + y[i]
            y2 = int(nu.random.uniform(0,2)) + y[i]
            self.makeWaterBody(x1, y1, x2, y2, const.POND_SPREAD)
            
        if(const.HAS_LAKE):
            self.makeWaterBody(24, 24, 26, 26, const.LAKE_SPREAD)
    
    # MEATHOD: makeWaterBody --------------------------------------------------  
    def makeWaterBody(self, x1, y1, x2, y2, spread):
        ax = min(x1,x2)
        bx = max(x1,x2)
        ay = min(y1,y2)
        by = max(y1,y2)
        
        x = ax
        y = ay
        while (x < bx or y < by):
            self.water_grid[y-spread*3:y+spread*3,\
                            x-spread*3:x+spread*3] = 0.5  
            if(x < bx):
                x += 1
            if(y < by):
                y += 1
       
        x = ax
        y = ay
        while (x < bx or y < by):         
            self.water_grid[y-spread*2:y+spread*2,\
                            x-spread*2:x+spread*2] = 0.75
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
    
    # MEATHOD: wheatherCheck --------------------------------------------------
    def wheatherCheck(self):
        check = False
        if(self.rained):
            check = True
        
        if(nu.random.uniform(0,1) < const.OVERCAST_CHANCE):
            self.light_grid *= 0.3
            if(nu.random.uniform(0,1) < const.RAIN_CHANCE):
                self.water_grid += 0.2
                self.rained = True
                check = False
        else:
            self.light_grid = nu.ones((self.length, self.width))
            for i in range(const.MAX_CLOUDS):
                if(nu.random.uniform(0,1) < const.CLOUD_CHANCE):
                    self.makeCloud()
                    
        if(check):
            self.water_grid -= 0.2
            self.rained = False
    
    # MEATHOD: makeCloud ------------------------------------------------------
    def makeCloud(self):
        x = int(nu.random.uniform(0,1) * 50)
        y = int(nu.random.uniform(0,1) * 50)
        
        thickness = nu.random.uniform(0.3,0.7)
        spreadX = int(nu.random.uniform(3,15))
        spreadY = int(nu.random.uniform(3,15))
        
        self.light_grid[y-spreadY:y+spreadY, x-spreadX:x+spreadX] *=\
            1-thickness
        
    # MEATHOD: updateTemp -----------------------------------------------------
    def updateTemp(self):
        self.temp_grid[:-1,:] = const.NATRUAL_TEMP
        self.temp_grid[:-1,:] += self.water_grid * const.WATER_TEMP
        self.temp_grid[:-1,:] += self.light_grid * const.LIGHT_TEMP
    
    # MEATHOD: makePlants -----------------------------------------------------
    def makePlants(self, chance):
        #Test every grid space for plant growth
        for y in range(self.length):
            for x in range(self.width):
                #Test for growth
                if nu.random.uniform(0,1) <= chance:
                    if(self.water_grid[y,x] < 0.75 and\
                       self.plant_grid[y,x] < 1 and self.burrow_grid[y,x] < 1):
                        #Make a grass plant
                        newPlant = fo.Grass(y,x)
                        self.plant_grid[y,x] = 1
                        self.plant_list.append(newPlant)
        #Grid and list should now be initialized
        
    # MEATHOD: initRabbits ----------------------------------------------------
    def initRabbits(self):
        #This rabbit spawn is hardcoded so we could keep them away from
        #their predators
        i = 0
        while(i < const.NUM_BURROWS):
            x = int(nu.random.uniform(2,self.width - 2))
            y = int(nu.random.uniform(2,self.length - 2))
            if(self.water_grid[y,x] < 0.75 and self.burrow_grid[y,x] < 1):
                self.burrow_grid[y,x] = 1
                i += 1
            
        self.spawnRabbits()
    
    # MEATHOD: spawnRabbits ---------------------------------------------------
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
                    
                    for j in range(const.RABBITS_PER_BURROW):
                        if(len(self.herbivore_list) >= const.MAX_RABBITS):
                            return
                        
                        locX = x + placeX[j]
                        locY = y + placeY[j]
                        
                        newRab = fa.Rabbit(locY,locX)
                        #Spawns around the burrow
                        self.herbivore_list.append(newRab)
                        self.herbivore_grid[locY, locX] = 1
    
    # MEATHOD: initFoxes ------------------------------------------------------        
    def initFoxes(self):
        #This fox spawn is hardcoded so we could keep them away from vulnerable
        #animals
        
        for i in range(const.NUM_FOXES):
            x = int(nu.random.uniform(0,self.width))
            y = int(nu.random.uniform(0,self.length))
            newFox = fa.Fox(y,x)
            self.carnivore_list.append(newFox)
            self.carnivore_grid[y, x] = 1
     
    # MEATHOD: runADay --------------------------------------------------------
    def runADay(self):
        for i in range(const.HOURS_PER_DAY):
            self.iterations += 1
            for j in range(len(self.herbivore_list)):
                if(self.findWater(self.herbivore_list[j])):
                    if(self.forage(self.herbivore_list[j])):
                        self.randomWalk(self.herbivore_list[j])
            for j in range(len(self.carnivore_list)):
                for k in range(const.EXTRA_FOX_STEPS):
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
        
    # MEATHOD: runAWeek -------------------------------------------------------
    def runAWeek(self):
        for i in range(const.DAYS_PER_WEEK):
            self.runADay()
        self.makePlants(const.PLANT_REPOP_CHANCE)
    
    # MEATHOD: runAMonth ------------------------------------------------------
    def runAMonth(self):
        for i in range(const.WEEKS_PER_MONTH):
            self.runAWeek()
        self.spawnRabbits()

#==============================================================================
# END FILE
