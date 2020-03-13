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
    
    energy = None                # current fauna energy
    max_energy = None            # maximum fauna energy
    move_energy_cost = None      # energy cost of moving
    wait_energy_cost = None      # energy cost of waiting
    energy_value = None          # energy provided to animal if consumed
    hungry = None                # threshold for being hungry
    eat_amount = None            # maximum amount of energy gained by eating 
    starve = None                # threshold for dying of hunger
    
    water = None                 # current fauna water
    max_water = None             # maximum fauna water
    move_water_cost = None       # water cost of moving
    wait_water_cost = None       # water cost of waiting
    water_value = None           # water provided to animal if consumed
    thirsty = None               # threshold for being thirsty
    drink_amount = None          # maximum amount of water gained by drinking
    desiccate = None             # threshold for dying of thirst
    
    temp = None                  # current temperature
    cold = None                  # threshold for being cold
    hot = None                   # threshold for being hot
    froze = None                 # threshold for dying of cold
    boiled = None                # threshold for dying of heat
    
    position = None              # current position in environment
    alive = None                 # alive status flag

    # MEATHOD: init -----------------------------------------------------------
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
        """
        #Initializes energy and water through uniform distribution
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN,\
                                        self.INIT_ENERGY_MAX)
        self.water = nu.random.uniform(self.INIT_WATER_MIN,\
                                       self.INIT_WATER_MAX)
        
        #Initializes temperature depending on natural temperature and environment
        self.temp = self.natural_temp
        self.cold = self.natural_temp + const.COLD_OFFSET
        self.froze = self.natural_temp + const.FROZE_OFFSET
        self.hot = self.natural_temp + const.HOT_OFFSET
        self.boiled = self.natural_temp + const.BOILED_OFFSET
        
        #Initializes energy and water values for when fauna is consumed
        self.energy_value = self.max_energy * const.FAUNA_ENERGY_PERCENT
        self.water_value = self.max_water * const.FAUNA_WATER_PERCENT
        
        #Initializes threshold for when fauna becomes hungry and thirsty
        self.hungry = self.max_energy * const.HUNGRY_PERCENT
        self.thirsty = self.max_water * const.THIRSTY_PERCENT
        
        #Initializes threshold for when fauna dies from hunger or thirst
        self.starve = self.max_energy * const.STARVE_PERCENT
        self.desiccate = self.max_water * const.DESICCATE_PERCENT
        
        #Initializes energy and water costs of taking an action
        self.move_energy_cost = ((self.max_energy / const.ENERGY_MOVE_FACTOR)\
                                 / const.HOURS_PER_DAY)
        self.wait_energy_cost = self.move_energy_cost\
                                / const.ENERGY_WAIT_REDUCE 
        self.move_water_cost = ((self.max_water / const.WATER_MOVE_FACTOR)\
                                / const.HOURS_PER_DAY)
        self.wait_water_cost = self.move_water_cost / const.WATER_WAIT_REDUCE 
        
        #Initializes location in environment
        self.position = [y, x]
        self.alive = True           #Set fauna as alive

    # MEATHOD: eat ------------------------------------------------------------
    def eat(self, amount):
        """ Description: Updates the fauna's energy based on a given 
                         amount. If there is more food than the maximum
                         amount the fauna can eat, it will just eat
                         the max amount.
    
            Variables: 
            -self: instance of class
            -amount: variable change to energy level
                     assumed to be positive
                     
            Postconditions: energy is increased depending on amount of food
                            available when eat was called.
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
            
            Postconditions:
            Fauna's position data is updated. Temperature is updated depending
            on location. Energy and Water are reduced by the move cost.
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
            
            Postconditions:
            Energy and Water are reduced by the wait cost.
        """
        self.energy -= self.wait_energy_cost
        self.water -= self.wait_water_cost
    
    # MEATHOD: consumed -------------------------------------------------------    
    def consumed(self):
        """ Description: Fauna has been eaten and it returns the amount of energy and water
                         it provides.
        
            Variables:
            -self: instance of class
           
            Postconditions:
            Returns an energy and water value depending on fauna
            
        """
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
        #Compare current fauna condition to the thresholds
        num = -1

        if(self.alive):
            if(self.energy < self.starve):
                self.alive = False
                num = 0
            elif(self.water < self.desiccate):
                self.alive = False
                num = 1
            elif(self.temp <= self.froze):
                self.alive = False
                num = 2
            elif(self.temp >= self.boiled):
                self.alive = False
                num = 3

        return [self.alive, num]
    
    # MEATHOD: isHerbivore ----------------------------------------------------
    def isHerbivore(self):
        """ Description: Returns whether a fauna is an herbivore"""
        return False
    
    # MEATHOD: isCarnivore ----------------------------------------------------
    def isCarnivore(self):
        """ Description: Returns whether a fauna is a carnivore"""
        return False 
    
# CLASS: Herbivore ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Herbivore(Fauna):
    """ Description: Herbivore class for fauna. An animal that eats plants.
                     Inherits Fauna
    """
    
    # MEATHOD: isHerbivore ----------------------------------------------------
    def isHerbivore(self):
        """ Description: Returns whether a fauna is an herbivore"""
        return True

# CLASS: Carnivore ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Carnivore(Fauna):
    """ Description: Carnivore class for fauna. An animal that eats other
                     animals.
    """
    
    # MEATHOD: isCarnivore ----------------------------------------------------    
    def isCarnivore(self):
        """ Description: Returns whether a fauna is a carnivore"""
        return True
    
# CLASS: Rabbit +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
class Rabbit(Herbivore):
    
    """ Description: Rabbit Class
                     Rabbits roam around the environment, eating plants and looking for 
                     water if they are thirsty. They are spawned from rabbit burrows.
                     Inherits Herbivore
            
    
            Variables: 
            -self: instance of class
    """
    INIT_ENERGY_MIN = 900         # initialization minimum for energy
    INIT_ENERGY_MAX = 1000       # initialization range for energy
    INIT_WATER_MIN = 900          # initialization minimum for water
    INIT_WATER_MAX = 1000        # initialization range for water
    
    max_energy = 1000            # maximum amount of energy contained
    eat_amount = 100             # maximum amount of energy recovered from eating
    
    max_water = 1000             # maximum amount of water contained
    drink_amount = 500           # maximum amount of water recovered from drinking
    
    natural_temp = 5             # natural temperature
    
# CLASS: Fox ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
class Fox(Carnivore, Herbivore):
    """ Description: Fox Class
                     Foxes are both carnivores and herbivores. They will hunt
                     down rabbits by following their scent. They can also eat
                     plants to survive.
                     Inherits Herbivore, Carnivore
                     
    
    """
    
    INIT_ENERGY_MIN = 3500       # initialization minimum for energy
    INIT_ENERGY_MAX = 4000       # initialization range for energy
    INIT_WATER_MIN = 1250         # initialization minimum for water
    INIT_WATER_MAX = 1500       # initialization range for water
    
    max_energy = 5000           # maximum amount of energy contained
    eat_amount = 1000           # maximum amount of energy restored from eating
    
    max_water = 1500            # maximum amount of water contained
    drink_amount = 750          # maximum amount of water restored from drinking
    
    natural_temp = 10           # natural temperature

    # MEATHOD: init -----------------------------------------------------------
    def __init__(self, y, x):
        """ Description: Class constructor
    
            Variables: 
            -self: instance of class
            -x: x position
            -y: y position
            
            PostConditions: 
            One of the fauna objects are created.
        """
        #Initializes energy and water through uniform distribution
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN,\
                                        self.INIT_ENERGY_MAX)
        self.water = nu.random.uniform(self.INIT_WATER_MIN,\
                                       self.INIT_WATER_MAX)
        
        #Initializes temperature depending on natural temperature and environment
        self.temp = self.natural_temp
        self.cold = self.natural_temp + const.COLD_OFFSET
        self.froze = self.natural_temp + const.FROZE_OFFSET
        self.hot = self.natural_temp + const.HOT_OFFSET
        self.boiled = self.natural_temp + const.BOILED_OFFSET
        
        #Initializes energy and water values for when fauna is consumed
        self.energy_value = self.max_energy * const.FAUNA_ENERGY_PERCENT
        self.water_value = self.max_water * const.FAUNA_WATER_PERCENT
        
        #Initializes threshold for when fauna becomes hungry and thirsty
        self.hungry = self.max_energy * const.HUNGRY_PERCENT
        self.thirsty = self.max_water * const.THIRSTY_PERCENT
        
        #Initializes threshold for when fauna dies from hunger or thirst
        self.starve = self.max_energy * const.STARVE_PERCENT
        self.desiccate = self.max_water * const.DESICCATE_PERCENT
        
        #Initializes energy and water costs of taking an action
        self.move_energy_cost = ((self.max_energy / const.ENERGY_MOVE_FACTOR)\
                                 / const.HOURS_PER_DAY) / const.EXTRA_FOX_STEPS
        self.wait_energy_cost = self.move_energy_cost\
                                / const.ENERGY_WAIT_REDUCE 
        self.move_water_cost = ((self.max_water / const.WATER_MOVE_FACTOR)\
                                / const.HOURS_PER_DAY) / const.EXTRA_FOX_STEPS
        self.wait_water_cost = self.move_water_cost / const.WATER_WAIT_REDUCE 
        
        #Initializes location in environment
        self.position = [y, x]
        self.alive = True      #Set fauna as alive
#==============================================================================
# END FILE
