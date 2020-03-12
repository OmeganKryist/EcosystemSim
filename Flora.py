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

# PROGRAM CONSTANTS ----------------------------------------------------
# User Modifiable

ENERGY_LOSS = 0.9
WATER_LOSS = 0.5

#Time segments per day                                                      
DT = 24

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

    INIT_ENERGY_MIN = None         # initialization minimum for energy
    INIT_ENERGY_MAX = None       # initialization range for energy
    INIT_WATER_MIN = None          # initialization minimum for water
    INIT_WATER_MAX = None        # initialization range for water
    INIT_SIZE_MIN = None
    INIT_SIZE_MAX = None
    
    energy = None
    unit_extra_energy = None
    unit_energy_cost = None
    energy_per_unit = None
    photo_amount = None
    
    water = None
    unit_extra_water = None
    unit_water_cost = None
    water_per_unit = None
    drink_amount = None
    
    size = None
    max_units = None
    
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
        self.size = nu.random.uniform(self.INIT_SIZE_MIN, self.INIT_SIZE_MAX)
        self.energy = nu.random.uniform(self.INIT_ENERGY_MIN*self.size, self.INIT_ENERGY_MAX*self.size)
        self.water = nu.random.uniform(self.INIT_WATER_MIN*self.size, self.INIT_WATER_MAX*self.size)
        
        self.position = [y, x]
        self.alive = True

    # MEATHOD: photosynth ----------------------------------------------
    def photosynth(self, amount):
        """ Description: updates the flora's water value
    
            Variables: 
            -self: instance of class
            -amount: variable change to water value
                     assumed to be positive
        """
        self.energy += max(amount, self.photo_amount * self.size)
        maxEnergy = (self.unit_extra_energy + self.unit_energy_cost) * self.size
        self.energy = min(self.energy, maxEnergy)

    # MEATHOD: drink ---------------------------------------------------
    def drink(self, amount):
        """ Description: updates the flora's water value
    
            Variables: 
            -self: instance of class
            -amount: variable change to water value
                     assumed to be positive
        """
        self.water = max(amount, self.drink_amount * self.size)
        maxWater = (self.unit_extra_water + self.unit_water_cost) * self.size
        self.water = min(self.water, maxWater)

    # MEATHOD: growth --------------------------------------------------
    def growth(self):
        """ Description: updates the flora's size
    
            Variables: 
            -self: instance of class
        """
        for i in range(int(self.size)):
        
            if(self.energy >= self.unit_energy_cost and self.water >= self.unit_water_cost):
                self.energy = max(self.energy - self.unit_energy_cost, 0)
                self.water = max(self.water - self.unit_water_cost, 0)
            elif():
                self.size -= max(0, self.size - 1)
        
        # if both energy and water are positive
        if(self.energy >= self.unit_energy_cost and self.water >= self.unit_water_cost):
            self.size = min(self.max_units, self.size + 1)

    # MEATHOD: healthCheck ---------------------------------------------
    def healthCheck(self):
        """ Description: updates the alive status if needed
    
            Variables: 
            -self: instance of class

            Output: a boolean value indicating the life of the fauna
        """
        if(self.alive):
            if(self.size <= 0):
                self.alive = False
        return self.alive
    
    def consumed(self, units):
        # If animal can eat the whole plant, reduce plant size to 0 and return
        # all the energy it would have given.
        # variable energy is not plant energy, it is energy for the animal.
        energyValue = 0
        waterValue = 0
        
        if units >= self.size:
            energyValue = self.size * self.energy_per_unit
            waterValue = self.size * self.energy_per_unit
            self.size = 0
            self.alive = False
        else:
            self.size -= units
            energyValue = units * self.energy_per_unit
            waterValue = units * self.energy_per_unit
            self.energy = min(self.energy, (self.unit_extra_energy + self.unit_energy_cost) * self.size)
            self.water = min(self.water, (self.unit_extra_water + self.unit_water_cost) * self.size)
            
        return [energyValue, waterValue]

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

    INIT_ENERGY_MIN = 500         # initialization minimum for energy
    INIT_ENERGY_MAX = 1000       # initialization range for energy
    INIT_WATER_MIN = 500         # initialization minimum for water
    INIT_WATER_MAX = 1000        # initialization range for water
    INIT_SIZE_MIN = 3
    INIT_SIZE_MAX = 5
    
    max_units = 5
    
    unit_energy_cost = 500
    unit_extra_energy = 500
    energy_per_unit = unit_energy_cost * ENERGY_LOSS
    photo_amount = 1000
    
    unit_water_cost = 500
    unit_extra_water = 500
    water_per_unit = unit_water_cost * WATER_LOSS
    drink_amount = 1000
    
#=======================================================================
# END FILE
