# START FILE
#==============================================================================
# GENERAL DOCUMENTATION _______________________________________________________
""" 

    See code documentation for specifics on code functionality
"""

# ADDITIONAL DOCUMENTATION ____________________________________________________

# Modification History:
# - 3 Mar 2020: File Created

# Notes:
# - Written for Python 3.7
# - To test simply run the file in the canopy distribution of python
#  or through some other IDE like visual studio or spyder
# - Documentation style inspired by CSS 458 professor Johnny Lin

#==============================================================================
# PROGRAM CONSTANTS ___________________________________________________________
# User modifiable

# ECOSYSTEM FILE
GRID_X = 50                     # Grid length
GRID_Y = 50                     # Grid Width

# Sim execution itterations
NUM_SIMS = 3                    # Number of Sims to run for each 
NUM_MONTHS = 2                  # Number of Months (if sim is by months)
NUM_WEEKS = 2                   # Number of Weeks (if sim is by weeks)
NUM_DAYS = 2                    # Number of Days (if sim is by Days)

# Time units (sim update by hour)
WEEKS_PER_MONTH = 4             # Number of weeks in a month
DAYS_PER_WEEK = 7               # Number of days in a week
HOURS_PER_DAY = 24              # Number of hours in a day

# effects lighting
MAX_CLOUDS = 10                 # Max number of clouds at a time
CLOUD_CHANCE = 0.6              # Chance a cloud spawns
OVERCAST_CHANCE = 0.2           # Chance for overcast weather (no visable sun)
RAIN_CHANCE = 0                 # Chance for Rain

# effects water
LAKE_SPREAD = 2                 # Size of lake
HAS_LAKE = True                 # Determins if the sime has a central lake
POND_SPREAD = 3                 # Size of ponds
NUM_PONDS = 0                   # Number of possible ponds
MIN_MOISTURE = 0.25             # Min water value at each tile

# effects temp
WATER_TEMP = -10                # Impact water has on location temp
LIGHT_TEMP = 5                  # Impact light has on location temp
NATRUAL_TEMP = 0                # Natrual temperture offset 
MAX_TEMP = 32                   # Maximum possible temp
MIN_TEMP = -32                  # Minimum possible temp

# effects scent
DISSIPATION_RATE = 0.9          # Dispation rate of the animal's scent trail
DISSIPATION_SPREAD = 0.8        # Dispation value to cells around scent trail
SCENT_SPREAD = 1                # how far the scent spreads from trail 

# effects plants
PLANT_CHANCE = 0.4              # Chance a cell initalizes with a plant
PLANT_REPOP_CHANCE = 0.1        # Chance a plant repopulates a cell during sim 
ENERGY_ABSORB_FACTOR = 1000     # Scaling value for plant photosynthsis
WATER_ABSORB_FACTOR = 1000      # Scaling value for plant drinking
PLANT_UNITS_TO_EAT = 2          # Number of units animals eat from plants

# effects  animals
RABBITS_PER_BURROW = 5          # Number of rabbits that spawn from a burrow
MAX_RABBITS = 100               # Maximum allowed rabbits in sim
NUM_BURROWS = 5                 # Number of burrows to generate in sim
NUM_FOXES = 3                   # Number of foxes to initalize 
MOVE_CHANCE = 0.5               # Chance an animal chooses to move randomly

# FAUNA FILE
FAUNA_ENERGY_PERCENT = 0.7      # Percent of max energy goten from consume
FAUNA_WATER_PERCENT = 0.1       # Percent of max water goten from consume

HUNGRY_PERCENT = 0.9            # Fauna hungry threshold percent 
STARVE_PERCENT = 0.6            # Fauna food death threshold percent 

THIRSTY_PERCENT = 0.6           # Fauna thrist threshold percent 
DESICCATE_PERCENT = 0.4         # Fauna water death threshold percent

COLD_OFFSET = -10               # Fauna cold threshold offset 
FROZE_OFFSET = -20              # Fauna chill death threshold offset 

HOT_OFFSET = 10                 # Fauna hot threshold offset 
BOILED_OFFSET = 20              # Fauna heat death threshold offset 

ENERGY_MOVE_FACTOR = 6          # Scales move cost by max energy divid this
ENERGY_WAIT_REDUCE = 2          # Energy cost reduction from moving (by divid)
WATER_MOVE_FACTOR = 8           # Scales move cost by max water divid this
WATER_WAIT_REDUCE = 2           # Water cost reduction from moving (by divid)

TEMP_TRANSFER = 0.2             # Percent of temp difference to impact fauna

EXTRA_FOX_STEPS = 3             # Number of extra moves the foxes can make

# FLORA FILE
FLORA_ENERGY_PERCENT = 0.1      # Percent of max energy goten from consume
FLORA_WATER_PERCENT = 0.05      # Percent of max water goten from consume

#==============================================================================
# END FILE
