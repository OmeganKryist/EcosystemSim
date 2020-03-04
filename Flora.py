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
INIT_SIZE_RANGE = 0         # initialization range for size (Max patch of grass)
GROWTH_UNIT = 0             # growth unit (14 days to reach max)
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
# CLASS: Grass ---------------------------------------------------------
class Grass(Flora):
    """
    Constant definitions are currently based off bluegrass as rabbits primarily eat
    grass. Bluegrass is common in our state.
    
    If we want to consider weeds, weeds in Washington state can be found here: 
    https://s3.wp.wsu.edu/uploads/sites/2072/2013/10/InvasiveWeedsEastWAEM005Epdf.pdf
    If we choose to add a weed, meadow hawkweed is a top contender.
    """
    #Assuming 1 grid of grass at max growth can feed about 2 rabbits.
    #An average rabbit needs about 105 calories daily
    
    # energy
    INIT_ENERGY_MIN = 0         # initialization minimum for energy
    INIT_ENERGY_RANGE = 200     # initialization range for energy
    ENERGY_CAPACITY = 200       # maximum energy that can be stored
    GROWTH_ENERGY_COST = 0      # energy cost of one growth unit
    
    # water
    INIT_WATER_MIN = 1          # initialization minimum for water
    INIT_WATER_RANGE = 1        # initialization range for water
    WATER_CAPACITY = 17 * 100   # maximum water that can be stored
    GROWTH_WATER_COST = 0       # water cost of one growth unit
    
    # size
    INIT_SIZE_MIN = 5*100       # initialization minimum for size
    INIT_SIZE_RANGE = 15 * 100  # initialization range for size
    GROWTH_UNIT = 1.43 * 100    # growth unit (14 days to reach max)
    DECAY_UNIT = 0.001          # decay unit (700 days to fully decay)
    #Max size of grass should be 20 * 100
    
    def __init__(self):
        self.size = rand.random() * INIT_SIZE_RANGE + INIT_SIZE_MIN
        #Water and energy values should be dependent on size of plant
        
        #Grass is 85% water but we may need to recalibrate this value
        self.water = self.size * 0.85
        self.energy = self.size * 0.15
        
    def consumed(self, amount):
        #If animal can eat the whole plant, reduce plant size to 0 and return
        #all the energy it would have given.
        #variable energy is not plant energy, it is energy for the animal.
        if amount >= self.size:
            energy = self.size
            self.size = 0
        else:
            self.size -= amount
            energy = amount
        return energy
    

#=======================================================================
# END FILE
