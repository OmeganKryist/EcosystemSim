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
import Variables as const

#======================================================================
# Analysis Functions --------------------------------------------------
def anRabToPlant(perBurrow, numBurrows):
    # grab values for restoring values
    hold1 = const.RABBITS_PER_BURROW
    hold2 = const.NUM_BURROWS
    
    #Parameters passed
    const.RABBITS_PER_BURROW = perBurrow # must be less than 9
    const.NUM_BURROWS = numBurrows
    
    beginningPlants = []
    endPlants = []
    
    print("Rabbits per Burrow: ", perBurrow)
    print("Burrows:", numBurrows)
    print("TotalRabbits:", perBurrow * numBurrows)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        beginningPlants.append(len(eco.plant_list))
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endPlants.append(len(eco.plant_list))
        
    avgBeginning = sum(beginningPlants) / len(beginningPlants)
    avgEnd = sum(endPlants) / len(endPlants)
    print("# Simulations:", const.NUM_SIMS)
    print("Average plants at beginning:", avgBeginning)
    print("Average plants at end:", avgEnd)
    print("Average plant difference:", avgBeginning - avgEnd, "\n")
    
    # restore values
    const.RABBITS_PER_BURROW = hold1
    const.NUM_BURROWS = hold2
    
def anLakeToRab(spread):
    hold = const.LAKE_SPREAD # grab value for restoring value
    
    const.LAKE_SPREAD = spread
    print("Lake Spread:", spread)
    endRabbits = []
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()
        for i in range(const.NUM_DAYS):
            eco.runADay()  
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits at end:", avgEnd)
    
    const.LAKE_SPREAD = hold # restore value
    
def anDissipationtoRab(dis):
    hold = const.DISSIPATION_RATE # grab value for restoring value
    
    const.DISSIPATION_RATE = dis
    print("Dissipation Rate:", dis)
    endRabbits = []
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()
        for i in range(const.NUM_DAYS):
            eco.runADay()  
        endRabbits.append(len(eco.herbivore_list))
    
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits at end:", avgEnd, "\n")
    
    const.DISSIPATION_RATE = hold # restore value
    
def anFoxToRab(fox):
    hold = const.NUM_FOXES # grab value for restoring value
    
    const.NUM_FOXES = fox
    print("Foxes:", fox)
    endRabbits = []
    dayExtinct = []
    
    lastDay = 0
    for j in range(const.NUM_SIMS):
        lastDay = 10
        eco = sim.EcoSystem()
        for i in range(const.NUM_DAYS):
            eco.runADay()  
            #Check if all rabbits are dead
            if len(eco.herbivore_list) == 0:
                if i < lastDay:
                    lastDay = i
        dayExtinct.append(lastDay)
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    avgDay = sum(dayExtinct) / len(dayExtinct)
    print("# Simulations:", const.NUM_SIMS)
    
    print("Average rabbits at end:", avgEnd)
    print("Average day eliminated:", avgDay, "\n")
    
    const.NUM_FOXES = hold # restore value
    
# SIMULATION TEST -------------------------------------------------------------
def testSim():
    eco = sim.EcoSystem()
    for i in range(1):
        eco.frame += 1
        eco.runAMonth()
        eco.displayGrids()
    eco.displayResults()

#=======================================================================   
# PROGRAM SCRIPT ------------------------------------------------------
# Driver code for program

testSim()

#======================================================================
# END FILE
