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
import Ecosystem as sim

# PROGRAM CONSTANTS ----------------------------------------------------
# User modifiable

# ECOSYSTEM
GRID_X = 50                     # var meaning
GRID_Y = 50

NUM_SIMS = 10
NUM_MONTHS = 2
NUM_WEEKS = 4
NUM_DAYS = 7
WEEKS_PER_MONTH = 4
DAYS_PER_WEEK = 7
HOURS_PER_DAY = 24

# effects lighting
MAX_CLOUDS = 10
CLOUD_CHANCE = 0.6
OVERCAST_CHANCE = 0.2
RAIN_CHANCE = 0.8

# effects water
LAKE_SPREAD = 4
HAS_LAKE = True # bool
POND_SPREAD = 1
NUM_PONDS = 0

# effects temp
WATER_TEMP = -2
LIGHT_TEMP = 2
NATRUAL_TEMP = 10
MAX_TEMP = 32
MIN_TEMP = -32

DISSIPATION_RATE = 0.9
DISSIPATION_SPREAD = 0.8
SCENT_SPREAD = 1

PLANT_CHANCE = 0.9
PLANT_REPOP_CHANCE = 0.1
ENERGY_ABSORB_FACTOR = 1000
WATER_ABSORB_FACTOR = 1000
PLANT_UNITS_TO_EAT = 2

RABBITS_PER_BURROW = 5 # must be less than 9
MAX_RABBITS = 100
NUM_BURROWS = 5

NUM_FOXES = 3

MOVE_CHANCE = 0.5

# FAUNA
FAUNA_ENERGY_PERCENT = 0.3
FAUNA_WATER_PERCENT = 0.1

HUNGRY_PERCENT = 0.9
STARVE_PERCENT = 0.5

THIRSTY_PERCENT = 0.4
DESICCATE_PERCENT = 0.2

COLD_OFFSET = -10
FROZE_OFFSET = -20

HOT_OFFSET = 10
BOILED_OFFSET = 20

ENERGY_MOVE_FACTOR = 6
ENERGY_WAIT_REDUCE = 2
WATER_MOVE_FACTOR = 8
WATER_WAIT_REDUCE = 2

TEMP_TRANSFER = 0.2

EXTRA_FOX_STEPS = 3

# FLORA
FLORA_ENERGY_PERCENT = 0.1
FLORA_WATER_PERCENT = 0.05

# PROGRAM GLOBALS ------------------------------------------------------
# Not User Modifiable

var = 0                     # var meaning

#======================================================================
# END FILE
