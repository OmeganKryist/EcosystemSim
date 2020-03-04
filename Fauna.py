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
import random as rand

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

# energy
INIT_ENERGY_MIN = 0         # initialization minimum for energy
INIT_ENERGY_RANGE = 0       # initialization range for energy
WAIT_ENERGY_COST = 0        # energy cost of not moving
MOVE_ENERGY_COST = 0        # energy cost of moving
STARVE = 0                  # value to which an animal dies if it's
                            # energy value is lower than 

# water
INIT_WATER_MIN = 0          # initialization minimum for water
INIT_WATER_RANGE = 0        # initialization range for water
WAIT_WATER_COST = 0         # water cost of not moving
MOVE_WATER_COST = 0         # water cost of moving
DESICCATE = 0               # value to which an animal dies if it's
                            # water value is lower than 

# PROGRAM GLOBALS ------------------------------------------------------
# Not User Modifiable

var = 0                     # var meaning

#=======================================================================
# CLASS: Fauna ---------------------------------------------------------
class Fauna:
    """ Description: Parent class for all fauna, provides very basic
                     functions and status
    
        Variables: 
        -energy: the fauna's energy level
        -water: the fauna's water level
        -position: the fauna's physical position in the simulation grid
        -alive: a boolean for checking if the animal is alive
    """
    energy = None
    water = None
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
        self.position = [x, y]
        self.alive = True

    # MEATHOD: eat -----------------------------------------------------
    def eat(self, amount):
        """ Description: updates the fauna's energy based on a given 
                         amount
    
            Variables: 
            -self: instance of class
            -amount: variable change to energy level
                     assumed to be positive
        """
        self.energy += amount

    # MEATHOD: drink ---------------------------------------------------
    def drink(self, amount):
        """ Description: updates the fauna's position
    
            Variables: 
            -self: instance of class
            -amount: variable change to water level
                     assumed to be positive
        """
        self.water += amount

    # MEATHOD: move ----------------------------------------------------
    def move(self, x, y):
        """ Description: updates the fauna's position
                         deducts the move cost
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        self.energy -= MOVE_ENERGY_COST
        self.water -= MOVE_WATER_COST
        self.position = [x, y]

    # MEATHOD: wait ----------------------------------------------------
    def wait(self):
        """ Description: deducts the wait cost
    
            Variables: 
            -self: instance of class
        """
        self.energy -= WAIT_ENERGY_COST
        self.water -= WAIT_WATER_COST

    # MEATHOD: randMove ------------------------------------------------
    def randMove(self, xRange, yRange):
        """ Description: provides a new possible location for the animal
    
            Variables: 
            -self: instance of class
            -xRange: x position
            -yRange: y position
        """
        x = xRange * (rand.random() * 2 - 1)
        y = yRange * (rand.random() * 2 - 1)
        return [x, y]

    # MEATHOD: healthCheck ---------------------------------------------
    def healthCheck(self):
        """ Description: updates the alive status if needed
    
            Variables: 
            -self: instance of class

            Output: a boolean value indicating the life of the fauna
        """
        if(self.energy < STARVE):
            self.alive = False
        if(self.water < DESICCATE):
            self.alive = False
        return self.alive
    
# CLASS: Herbivore -----------------------------------------------------
class Herbivore(Fauna):
    """ Description:
    
        Variables: 
        -var: 
    """
    # MEATHOD: INIT ----------------------------------------------------
    def __init__(self):
        """ Description: Class constructor
            
    
            Variables: 
            -self: instance of class
        """
    
# CLASS: Carnivore -----------------------------------------------------
class Carnivore(Fauna):
    """ Description:
    
        Variables: 
        -var:  
    """
    # MEATHOD: INIT ----------------------------------------------------
    def __init__(self):
        """ Description: Class constructor
            
    
            Variables: 
            -self: instance of class  
        """

#=======================================================================
# END FILE

