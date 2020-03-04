# START FILE
#=======================================================================
# GENERAL DOCUMENTATION ------------------------------------------------
""" 

    See code documentation for specifics on code functionality
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
import random as rand

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

# energy
INIT_ENERGY_MIN = 0         # initialization minimum for energy
INIT_ENERGY_RANGE = 0       # initialization range for energy
ENERGY_CAPACITY = 0         # maximum energy that can be stored
GROWTH_ENERGY_COST = 0      # energy cost of one growth unit

# water
INIT_WATER_MIN = 0          # initialization minimum for water
INIT_WATER_RANGE = 0        # initialization range for water
WATER_CAPACITY = 0          # maximum water that can be stored
GROWTH_WATER_COST = 0       # water cost of one growth unit

# size
INIT_SIZE_MIN = 0           # initialization minimum for size
INIT_SIZE_RANGE = 0         # initialization range for size
GROWTH_UNIT = 0             # growth unit
DECAY_UNIT = 0              # decay unit

# PROGRAM GLOBALS ------------------------------------------------------
# Not User Modifiable

var = 0                     # var meaning

# PROGRAM SCRIPT -------------------------------------------------------
# Driver code for program

#=======================================================================
# CLASS: Flora ---------------------------------------------------------
class Flora:
    """ Description:
    
        Variables: 
        -energy: the flora's energy level
        -water: the flora's water level
        -size: the flora's size level
        -position: the flora's physical position in the simulation grid
        -alive: a boolean for checking if the animal is alive
    """
    energy = None
    water = None
    size = None
    position = None
    alive = None
    # MEATHOD: INIT ----------------------------------------------------
    def __init__(self, x, y):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        self.energy = rand.random() * INIT_ENERGY_RANGE + INIT_ENERGY_MIN
        self.water = rand.random() * INIT_WATER_RANGE + INIT_WATER_MIN
        self.size = rand.random() * INIT_SIZE_RANGE + INIT_SIZE_MIN
        self.size *= GROWTH_UNIT
        self.position = [x, y]
        self.alive = True

    # MEATHOD: photosynth ----------------------------------------------
    def photosynth(self, amount):
        """ Description: updates the flora's water value
    
            Variables: 
            -self: instance of class
            -amount: variable change to water value
                     assumed to be positive
        """
        self.energy += amount

    # MEATHOD: drink ---------------------------------------------------
    def drink(self, amount):
        """ Description: updates the flora's water value
    
            Variables: 
            -self: instance of class
            -amount: variable change to water value
                     assumed to be positive
        """
        self.water += amount

    # MEATHOD: growth --------------------------------------------------
    def growth(self):
        """ Description: updates the flora's size
    
            Variables: 
            -self: instance of class
        """
        self.energy = max(self.energy - GROWTH_ENERGY_COST, 0)
        self.water = max(self.water - GROWTH_WATER_COST, 0)
        
        # if both energy and water are positive
        if(self.energy * self.water > 0):
            self.size += GROWTH_UNIT
        else:
            self.size -= DECAY_UNIT

    # MEATHOD: healthCheck ---------------------------------------------
    def healthCheck(self):
        """ Description: updates the alive status if needed
    
            Variables: 
            -self: instance of class

            Output: a boolean value indicating the life of the fauna
        """
        if(self.size <= 0):
            self.alive = False
        return self.alive

#=======================================================================
# END FILE
