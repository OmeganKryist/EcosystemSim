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
        length = 50
        width = 50
        #These grids are booleans(0/1) for when animals are at a location
        plant_grid = nu.zeros(length, width)
        herbivore_grid = nu.zeros(length, width)
        carnivore_grid = nu.zeros(length, width)
        
        #These lists hold every individual plant and animal
        plant_list = []
        herbivore_list = []
        carnivore_list = []
        
        self.initPlants()
        return 1

# FUNCTION: FUNC -------------------------------------------------------
def func():
    """ Description:
        
    
        Variables: 
        -var: 
    
        Output: 
    """
    return 2

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

