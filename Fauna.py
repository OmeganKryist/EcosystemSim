# START FILE
#==============================================================================
# GENERAL DOCUMENTATION -------------------------------------------------------
""" This file contains animal objects used in the ecosystem simulation.
    The simulation of these animals are done in the ecosystem file. Here, the
    animal-related variables are stored and modified.
    Animals in the herbivore class eat plants.
    Animals in the carnivore class eat other animals.
    Some animals can be both herbivores and carnivores.
    Current Animals: Rabbit, Fox
"""

# ADDITIONAL DOCUMENTATION ----------------------------------------------------
#Authors: Christian Rahmel, William Taing, Morgan Du Bois
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
import numpy as nu

#==============================================================================
# CLASS: Fauna ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
    
    temp = None
    cold = None
    hot = None
    froze = None
    boiled = None
    
    position = None
    alive = None

    # MEATHOD: init -----------------------------------------------------------
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN,\
                                        self.INIT_ENERGY_MAX)
        self.water = nu.random.uniform(self.INIT_WATER_MIN,\
                                       self.INIT_WATER_MAX)
        
        self.temp = self.natural_temp
        self.cold = self.natural_temp + const.COLD_OFFSET
        self.froze = self.natural_temp + const.FROZE_OFFSET
        self.hot = self.natural_temp + const.HOT_OFFSET
        self.boiled = self.natural_temp + const.BOILED_OFFSET
        
        self.energy_value = self.max_energy * const.FAUNA_ENERGY_PERCENT
        self.water_value = self.max_water * const.FAUNA_WATER_PERCENT
        
        self.hungry = self.max_energy * const.HUNGRY_PERCENT
        self.thirsty = self.max_water * const.THIRSTY_PERCENT
        
        self.starve = self.max_energy * const.STARVE_PERCENT
        self.desiccate = self.max_water * const.DESICCATE_PERCENT
        
        self.move_energy_cost = ((self.max_energy / const.ENERGY_MOVE_FACTOR)\
                                 / const.HOURS_PER_DAY)
        self.wait_energy_cost = self.move_energy_cost\
                                / const.ENERGY_WAIT_REDUCE 
        self.move_water_cost = ((self.max_water / const.WATER_MOVE_FACTOR)\
                                / const.HOURS_PER_DAY)
        self.wait_water_cost = self.move_water_cost / const.WATER_WAIT_REDUCE 
        
        self.position = [y, x]
        self.alive = True

    # MEATHOD: eat ------------------------------------------------------------
    def eat(self, amount):
        """ Description: updates the fauna's energy based on a given 
                         amount
    
            Variables: 
            -self: instance of class
            -amount: variable change to energy level
                     assumed to be positive
        """
        self.energy += min(amount, self.eat_amount)

    # MEATHOD: drink ----------------------------------------------------------
    def drink(self, amount):
        """ Description: updates the fauna's position
    
            Variables: 
            -self: instance of class
            -amount: variable change to water level
                     assumed to be positive
        """
        self.water += min(amount, self.drink_amount)

    # MEATHOD: move -----------------------------------------------------------
    def move(self, y, x, tempValue):
        """ Description: updates the fauna's position
                         deducts the move cost
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        if(tempValue < self.temp):
            self.temp = max(self.temp -\
                            (abs(tempValue) * const.TEMP_TRANSFER), tempValue)
        elif(tempValue > self.temp):
            self.temp = min(self.temp +\
                            (abs(tempValue) * const.TEMP_TRANSFER), tempValue)
        
        self.energy -= self.move_energy_cost
        self.water -= self.move_water_cost
        self.position = [y, x]

    # MEATHOD: wait -----------------------------------------------------------
    def wait(self):
        """ Description: deducts the wait cost
    
            Variables: 
            -self: instance of class
        """
        self.energy -= self.wait_energy_cost
        self.water -= self.wait_water_cost
    
    # MEATHOD: consumed -------------------------------------------------------    
    def consumed(self):
        self.alive = False # it's been eaten
        # return array of energy and water values to add to predators
        return [self.energy_value, self.water_value]

    # MEATHOD: healthCheck ----------------------------------------------------
    def healthCheck(self):
        """ Description: updates the alive status if needed
    
            Variables: 
            -self: instance of class

            Output: a boolean value indicating the life of the fauna
        """
        if(self.alive):
            if(self.energy < self.starve):
                self.alive = False
            elif(self.water < self.desiccate):
                self.alive = False
            elif(self.temp <= self.froze):
                self.alive = False
            elif(self.temp >= self.boiled):
                self.alive = False
        return self.alive
    
    # MEATHOD: isHerbivore ----------------------------------------------------
    def isHerbivore(self):
        return False
    
    # MEATHOD: isCarnivore ----------------------------------------------------
    def isCarnivore(self):
        return False 
    
# CLASS: Herbivore ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Herbivore(Fauna):
    """ Description:
    
        Variables: 
        -var: 
    """
    
    # MEATHOD: isHerbivore ----------------------------------------------------
    def isHerbivore(self):
        return True

# CLASS: Carnivore ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Carnivore(Fauna):
    """ Description:
    
        Variables: 
        -var:  
    """
    
    # MEATHOD: isCarnivore ----------------------------------------------------    
    def isCarnivore(self):
        return True
    
# CLASS: Rabbit +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
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
    
    natural_temp = 5
    
# CLASS: Fox ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
class Fox(Carnivore, Herbivore):
    """ Description: Modeled after the red fox, a native animal to Washington.
    
    """
    
    INIT_ENERGY_MIN = 3500       # initialization minimum for energy
    INIT_ENERGY_MAX = 4000       # initialization range for energy
    INIT_WATER_MIN = 1250         # initialization minimum for water
    INIT_WATER_MAX = 1500       # initialization range for water
    
    max_energy = 5000
    eat_amount = 1000
    
    max_water = 1500
    drink_amount = 750
    
    natural_temp = 10

    # MEATHOD: init -----------------------------------------------------------
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN,\
                                        self.INIT_ENERGY_MAX)
        self.water = nu.random.uniform(self.INIT_WATER_MIN,\
                                       self.INIT_WATER_MAX)
        
        self.temp = self.natural_temp
        self.cold = self.natural_temp + const.COLD_OFFSET
        self.froze = self.natural_temp + const.FROZE_OFFSET
        self.hot = self.natural_temp + const.HOT_OFFSET
        self.boiled = self.natural_temp + const.BOILED_OFFSET
        
        self.energy_value = self.max_energy * const.FAUNA_ENERGY_PERCENT
        self.water_value = self.max_water * const.FAUNA_WATER_PERCENT
        
        self.hungry = self.max_energy * const.HUNGRY_PERCENT
        self.thirsty = self.max_water * const.THIRSTY_PERCENT
        
        self.starve = self.max_energy * const.STARVE_PERCENT
        self.desiccate = self.max_water * const.DESICCATE_PERCENT
        
        self.move_energy_cost = ((self.max_energy / const.ENERGY_MOVE_FACTOR)\
                                 / const.HOURS_PER_DAY) / const.EXTRA_FOX_STEPS
        self.wait_energy_cost = self.move_energy_cost\
                                / const.ENERGY_WAIT_REDUCE 
        self.move_water_cost = ((self.max_water / const.WATER_MOVE_FACTOR)\
                                / const.HOURS_PER_DAY) / const.EXTRA_FOX_STEPS
        self.wait_water_cost = self.move_water_cost / const.WATER_WAIT_REDUCE 
        
        self.position = [y, x]
        self.alive = True
#==============================================================================
# END FILE
