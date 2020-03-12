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

# PROGRAM CONSTANTS ------------------------------------------------------
# User Modifiable

ENERGY_LOSS = 0.1
WATER_LOSS = 0.05

HUNGRY_PERCENT = 0.8
STARVE_PERCENT = 0.4
THIRSTY_PERCENT = 0.6
DESICCATE_PERCENT = 0.2

ENERGY_MOVE_FACTOR = 8
ENERGY_WAIT_REDUCE = 2
WATER_MOVE_FACTOR = 2
WATER_WAIT_REDUCE = 4

#Time segments per day                                                      
DT = 24



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
    
    INIT_ENERGY_MIN = None         # initialization minimum for energy
    INIT_ENERGY_MAX = None       # initialization range for energy
    INIT_WATER_MIN = None          # initialization minimum for water
    INIT_WATER_MAX = None        # initialization range for water
    
    energy = None
    max_energy = None
    move_energy_cost = None
    wait_energy_cost = None
    energy_value = None
    hungry = None
    eat_amount = None
    starve = None
    
    water = None
    max_water = None
    move_water_cost = None
    wait_water_cost = None
    water_value = None
    thirsty = None
    drink_amount = None
    desiccate = None
    
    position = None
    alive = None

    # MEATHOD: init ----------------------------------------------------
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN, self.INIT_ENERGY_MAX)
        self.water = nu.random.uniform(self.INIT_WATER_MIN, self.INIT_WATER_MAX)
        
        self.energy_value = self.max_energy * ENERGY_LOSS
        self.water_value = self.max_water * WATER_LOSS
        
        self.hungry = self.max_energy * HUNGRY_PERCENT
        self.thirsty = self.max_water * THIRSTY_PERCENT
        
        self.starve = self.max_energy * STARVE_PERCENT
        self.desiccate = self.max_water * DESICCATE_PERCENT
        
        self.move_energy_cost = (self.max_energy / ENERGY_MOVE_FACTOR) / DT
        self.wait_energy_cost = self.move_energy_cost / ENERGY_WAIT_REDUCE 
        self.move_water_cost = (self.max_water / WATER_MOVE_FACTOR) / DT
        self.wait_water_cost = self.move_water_cost / WATER_WAIT_REDUCE 
        
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
        self.energy += min(amount, self.eat_amount)

    # MEATHOD: drink ---------------------------------------------------
    def drink(self, amount):
        """ Description: updates the fauna's position
    
            Variables: 
            -self: instance of class
            -amount: variable change to water level
                     assumed to be positive
        """
        self.water += min(amount, self.drink_amount)

    # MEATHOD: move ----------------------------------------------------
    def move(self, y, x):
        """ Description: updates the fauna's position
                         deducts the move cost
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        self.energy -= self.move_energy_cost
        self.water -= self.move_water_cost
        self.position = [y, x]

    # MEATHOD: wait ----------------------------------------------------
    def wait(self):
        """ Description: deducts the wait cost
    
            Variables: 
            -self: instance of class
        """
        self.energy -= self.wait_energy_cost
        self.water -= self.wait_water_cost
        
    def consumed(self):
        self.alive = False # it's been eaten
        # return array of energy and water values to add to predators
        return [self.energyValue, self.waterValue]

    # MEATHOD: healthCheck ---------------------------------------------
    def healthCheck(self):
        """ Description: updates the alive status if needed
    
            Variables: 
            -self: instance of class

            Output: a boolean value indicating the life of the fauna
        """
        if(self.alive):
            if(self.energy < self.starve):
                self.alive = False
            if(self.water < self.desiccate):
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
    INIT_ENERGY_MIN = 900         # initialization minimum for energy
    INIT_ENERGY_MAX = 1000       # initialization range for energy
    INIT_WATER_MIN = 900          # initialization minimum for water
    INIT_WATER_MAX = 1000        # initialization range for water
    
    max_energy = 1000
    eat_amount = 100
    
    max_water = 1000
    drink_amount = 500

# CLASS: Carnivore -----------------------------------------------------
class Carnivore(Fauna):
    """ Description:
    
        Variables: 
        -var:  
    """
        
    def isCarnivore(self):
        return True
        
class Fox(Carnivore, Herbivore):
    """ Description: Modeled after the red fox, a native animal to Washington.
    
    """
    
    INIT_ENERGY_MIN = 1000       # initialization minimum for energy
    INIT_ENERGY_MAX = 1500       # initialization range for energy
    INIT_WATER_MIN = 900         # initialization minimum for water
    INIT_WATER_MAX = 1000       # initialization range for water
    
    max_energy = 2000
    eat_amount = 200
    
    max_water = 1000
    drink_amount = 500

#=======================================================================
# END FILE
