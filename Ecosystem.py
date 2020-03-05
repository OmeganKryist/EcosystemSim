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
import Fauna as fa
import Flora as fo

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

VAR = 0                     # var meaning

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
    
    
    
    # MEATHOD: INIT ----------------------------------------------------
    def __init__(self):
        """ Description: Class constructor
            
    
            Variables: 
            -var: 
    
            Output: 
        """
        #Grid Size variables
        self.length = 50
        self.width = 50
        #These grids are booleans(0/1) for when animals are at a location
        self.plant_grid = nu.zeros((self.length, self.width))
        self.herbivore_grid = nu.zeros((self.length, self.width))
        self.carnivore_grid = nu.zeros((self.length, self.width))
        
        #These lists hold every individual plant and animal
        self.plant_list = []
        self.herbivore_list = []
        self.carnivore_list = []
        
        self.initPlants()
        return

# FUNCTION: FUNC -------------------------------------------------------
    def func():
        """ Description:
            
        
            Variables: 
            -var: 
        
            Output: 
        """
        return 2
    
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
        violation = nu.where(nu.logical_or( \
        nu.logical_or(moveY >= self.length, moveY < 0),\
        nu.logical_or(moveX >= self.width, moveX < 0)))
        
        #Delete areas that cross borders
        nu.delete(moveX, violation)
        nu.delete(moveY, violation)
        
        index = nu.arange(len(moveX))
        nu.shuffle(index)
        
        #moveX and moveY may need to switch 
        Fauna.position(moveX[index[0]], moveY[index[0]])
        
        return
        
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
        return
#=======================================================================
# END FILE