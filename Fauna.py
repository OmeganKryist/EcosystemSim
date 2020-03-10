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
                            #water value is lower than 
  
#Time segments per day                                                      
dt = 1 / 24

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
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        self.energy = rand.random() * INIT_ENERGY_RANGE + INIT_ENERGY_MIN
        self.water = rand.random() * INIT_WATER_RANGE + INIT_WATER_MIN
        self.position = [y, x]
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
    def move(self, y, x):
        """ Description: updates the fauna's position
                         deducts the move cost
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        self.energy -= MOVE_ENERGY_COST
        self.water -= MOVE_WATER_COST
        self.position = [y, x]

    # MEATHOD: wait ----------------------------------------------------
    def wait(self):
        """ Description: deducts the wait cost
    
            Variables: 
            -self: instance of class
        """
        self.energy -= WAIT_ENERGY_COST
        self.water -= WAIT_WATER_COST

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
      
    def isHerbivore(self):
        return False
    
    def isCarnivore(self):
        return False 
    
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
    
    def isHerbivore(self):
        return True
        
class Rabbit(Herbivore):
    
    """ Description: Rabbit Class
        I read that rabbits need to eat 105 calories a day to maintain
        optimal health so their max energy is 1000 and they die within 6 days
        of not eating and 3 of not drinking. A rabbit should gain about 105
        energy when eating every day.
            
    
            Variables: 
            -self: instance of class
    """
    def __init__(self, y, x):
    # energy
        self.INIT_ENERGY_MIN = 900         # initialization minimum for energy
        self.INIT_ENERGY_RANGE = 100       # initialization range for energy
        self.WAIT_ENERGY_COST = 50 * dt    # energy cost of not moving
        self.MOVE_ENERGY_COST = 100  * dt   # energy cost of moving
        self.STARVE = 400                  # value to which an animal dies if it's
                                    # energy value is lower than 
        self.HUNGRY = 900                   #Threshold for when animal is hungry
        
        # water
        self.INIT_WATER_MIN = 900          # initialization minimum for water
        self.INIT_WATER_RANGE = 100        # initialization range for water
        self.WAIT_WATER_COST = 50 * dt     # water cost of not moving
        self.MOVE_WATER_COST = 100 * dt     # water cost of moving
        self.DESICCATE = 700               # value to which an animal dies if it's
                                    # water value is lower than 
        self.eatAmt = 105                   #Max amount that rabbit will eat at once
        
        self.THIRSTY = 900                  # Threshold for when animal is thirsty
                                    
        self.energy = rand.random() * self.INIT_ENERGY_RANGE + self.INIT_ENERGY_MIN
        self.water = rand.random() * self.INIT_WATER_RANGE + self.INIT_WATER_MIN
        
        self.position = [y, x]
        self.alive = True
        
    
    def consumed(self):
        #A rabbit provides 200 energy to predators
        energyValue = 200
        return energyValue

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
        
    def isCarnivore(self):
        return True
        
class Fox(Carnivore, Herbivore):
    """ Description: Modeled after the red fox, a native animal to Washington.
    
    """
    
    def __init__(self, y, x):
        self.INIT_ENERGY_MIN = 1000         # initialization minimum for energy
        self.INIT_ENERGY_RANGE = 200       # initialization range for energy
        self.WAIT_ENERGY_COST = 50 * dt    # energy cost of not moving
        self.MOVE_ENERGY_COST = 150 * dt   # energy cost of moving
        self.STARVE = 400                  # value to which an animal dies if it's
                                    # energy value is lower than 
        self.HUNGRY = 900                   #Threshold for when animal is hungry
        
        # water
        self.INIT_WATER_MIN = 900          # initialization minimum for water
        self.INIT_WATER_RANGE = 100        # initialization range for water
        self.WAIT_WATER_COST = 50 * dt        # water cost of not moving
        self.MOVE_WATER_COST = 100 * dt        # water cost of moving
        self.DESICCATE = 400               # value to which an animal dies if it's
                                    # water value is lower than 
        self.THIRSTY = 900                  # Threshold for when animal is thirsty
          
        self.eatAmt = 200                   #Max amount that fox will eat at once
                                    
        self.energy = rand.random() * self.INIT_ENERGY_RANGE + self.INIT_ENERGY_MIN
        self.water = rand.random() * self.INIT_WATER_RANGE + self.INIT_WATER_MIN
        
        self.position = [y, x]
        self.alive = True

#=======================================================================
# END FILE

