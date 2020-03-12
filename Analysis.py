# START FILE
#==============================================================================
# GENERAL DOCUMENTATION _______________________________________________________
""" 
    Ecosystem Analysis
    This file contains functions that modify the constants of the Ecosystem
    simulation. By changing the parameters of a function, the model will be
    modified. We can observe the results of changing the constants here.
    
    Functions:
        anRabToPlant - Changes amount of rabbits
        anLakeToRab - Changes size of lake
        anDissipationtoRab - Changes scent dissipation rate
        anFoxToRab - Changes amount of foxes
        anPondToRab - Changes amount and size of ponds
        anFoxStepToRab - Changes extra amount of steps foxes get over rabbits
        anEnergyToAnimals - Changes energy costs for animals throughout a day
        anHungerToAnimals - Changes threshold where animals get hungry or starve
        anThirstToAnimals - Changes threshold where animals get thirsty or dessicate
        anPlantChanceToAnimals - Changes amount of plants spawned in initialization
        anPlantStatsToAnimals - Changes energy and water values of plants
        
    Output:
        Results of the simulation in text and visualized in grid form.
    
    See code documentation for specifics on code functionality
"""

# ADDITIONAL DOCUMENTATION ____________________________________________________
#
#Authors: Christian Raheml, William Taing, Morgan Du Bois
# Modification History:
# - 3 Mar 2020: File Created

# Notes:
# - Written for Python 3.7
# - To test simply run the file in the canopy distribution of python
#  or through some other IDE like visual studio or spyder
# - Documentation style inspired by CSS 458 professor Johnny Lin

#==============================================================================
# PROGRAM IMPORTS _____________________________________________________________
import Ecosystem as sim
import Variables as const

# ANALYSIS FUNCTIONS __________________________________________________________
# FUNCTION: anRabToPlant ------------------------------------------------------
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

# FUNCTION: anLakeToRab -------------------------------------------------------    
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

# FUNCTION: anDissipationtoRab ------------------------------------------------    
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

# FUNCTION: anFoxToRab --------------------------------------------------------    
def anFoxToRab(fox):
    hold = const.NUM_FOXES # grab value for restoring value
    
    const.NUM_FOXES = fox
    print("Foxes:", fox)
    endRabbits = []
    dayExtinct = []
    
    lastDay = 0
    for j in range(const.NUM_SIMS):
        lastDay = NUM_DAYS
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
 
# FUNCTION: anPondToRab --------------------------------------------------------   
def anPondToRab(ponds, pondSpread):
    hold = const.NUM_PONDS      # grab value for restoring value
    const.NUM_PONDS = ponds     
    hold2 = const.POND_SPREAD
    const.POND_SPREAD = pondSpread
    
    endRabbits = []
    
    print("Ponds: ", ponds)
    print("Pond Spread:", pondSpread)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEnd, "\n")
    
    const.NUM_PONDS = hold      # restore value
    const.POND_SPREAD = hold2
 
# FUNCTION: anFoxStepToRab -------------------------------------------------------- 
def anFoxStepToRab(steps):
    hold = const.EXTRA_FOX_STEPS        # grab value for restoring value
    const.EXTRA_FOX_STEPS = steps
    
    
    endRabbits = []
    
    print("Extra Fox Steps (Per 1 Rabbit Step): ", steps)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        
    avgEnd = sum(endRabbits) / len(endRabbits)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEnd, "\n")
    
    const.EXTRA_FOX_STEPS = hold
 
# FUNCTION: anEnergyToAnimals -------------------------------------------------
def anEnergyToAnimals(enMove, enWait, waMove, waWait):
    """
        enMove = Energy Cost Moving
        enWait = Energy cost waiting
        enMove = Energy cost moving in water
        enWait = Energy cost waiting in water
    """
    hold = const.ENERGY_MOVE_FACTOR         # grab value for restoring value
    const.ENERGY_MOVE_FACTOR = enMove
    hold2 = const.ENERGY_WAIT_REDUCE
    const.ENERGY_WAIT_FACTOR = enWait
    hold3 = const.WATER_MOVE_FACTOR
    const.WATER_MOVE_FACTOR = waMove
    hold4 = const.WATER_WAIT_REDUCE
    const.WATER_WAIT_FACTOR = waWait

    
    endRabbits = []
    endFoxes = []
    
    print("Move Energy Cost Factor: ", enMove)
    print("Wait Energy Reduction: ", enWait)
    print("Water Move Energy Cost Factor: ", waMove)
    print("Water Wait Energy Reduction: ", waWait)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEndR)
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.ENERGY_MOVE_FACTOR = hold         # restore value
    const.ENERGY_WAIT_REDUCE = hold2
    const.WATER_MOVE_FACTOR = hold3
    const.WATER_WAIT_REDUCE = hold4
 
# FUNCTION: anHungerToAnimals -------------------------------------------------
def anHungerToAnimals(hunger, starve):
    hold = const.HUNGRY_PERCENT         # grab value for restoring value
    const.HUNGRY_PERCENT = hunger
    hold2 = const.STARVE_PERCENT
    const.STARVE_PERCENT = starve
    
    endRabbits = []
    endFoxes = []
    
    print("Energy Hungry Percentage: ", hunger)
    print("Energy Starvation Percentage: ", starve)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEndR, "\n")
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.HUNGRY_PERCENT = hold      # restore value
    const.STARVE_PERCENT = hold2
    
# FUNCTION: anThirstToAnimals -------------------------------------------------    
def anThirstToAnimals(thirst, dessicate):
    hold = const.THIRSTY_PERCENT         # grab value for restoring value
    const.THIRSTY_PERCENT = thirst
    hold2 = const.DESICCATE_PERCENT
    const.DESICCATE_PERCENT = dessicate
    
    endRabbits = []
    endFoxes = []
    
    print("Water Thirsty Percentage: ", thirst)
    print("Water Dessicate Percentage: ", dessicate)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEndR)
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.THIRSTY_PERCENT = hold      # restore value
    const.DESICCATE_PERCENT = hold2
    
# FUNCTION: anPlantChanceToAnimals --------------------------------------------    
def anPlantChanceToAnimals(plantChance):
    hold = const.PLANT_CHANCE         # grab value for restoring value
    const.PLANT_CHANCE = plantChance
    
    endRabbits = []
    endFoxes = []
    beginningPlants = []
    
    print("Plant Growth Chance (Initial): ", plantChance)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        beginningPlants.append(len(eco.plant_list))
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgPlant = sum(beginningPlants) / len(beginningPlants)
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average Plants Grown (Initially)", avgPlant)
    print("Average rabbits survived:", avgEndR)
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.PLANT_CHANCE = hold      # restore value
    
# FUNCTION: anPlantChanceToAnimals --------------------------------------------  
def anPlantRepopToAnimals(plantRepop):
    hold = const.PLANT_REPOP_CHANCE         # grab value for restoring value
    const.PLANT_REPOP_CHANCE = plantRepop
    
    endRabbits = []
    endFoxes = []
    
    print("Plant Growth Chance (Initial): ", plantRepop)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEndR)
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.PLANT_REPOP_CHANCE = hold      # restore value
    
# FUNCTION: anPlantStatsToAnimals ---------------------------------------------  
def anPlantStatsToAnimals(energy, water):
    hold = const.FLORA_ENERGY_PERCENT         # grab value for restoring value
    const.FLORA_ENERGY_PERCENT = energy
    hold2 = const.FLORA_WATER_PERCENT
    const.FLORA_WATER_PERCENT = water
    
    endRabbits = []
    endFoxes = []
    
    print("Plant Energy Percent: ", energy)
    print("Plant Water Percent: ", water)
    print("Rabbits:", const.NUM_BURROWS * const.RABBITS_PER_BURROW)
    print("Foxes:", const.NUM_FOXES)
    
    for j in range(const.NUM_SIMS):
        eco = sim.EcoSystem()           #Initialize Ecosystem
        for i in range(const.NUM_DAYS):
            eco.runADay()
        endRabbits.append(len(eco.herbivore_list))
        endFoxes.append(len(eco.carnivore_list))
        
    avgEndR = sum(endRabbits) / len(endRabbits)
    avgEndF = sum(endFoxes) / len(endFoxes)
    print("# Simulations:", const.NUM_SIMS)
    print("Average rabbits survived:", avgEndR)
    print("Average foxes survived:", avgEndF, "\n") 
    
    const.FLORA_ENERGY_PERCENT = hold      # restore value
    const.FLORA_WATER_PERCENT = hold2
    
# SIMULATION TESTS ____________________________________________________________
# FUNCTION: testSim -----------------------------------------------------------
def testSim():
    eco = sim.EcoSystem()
    for i in range(1):
        eco.frame += 1
        eco.runAMonth()
        eco.displayGrids()
    eco.displayResults()

# PROGRAM SCRIPT ______________________________________________________________
# Driver code for program

testSim()

#==============================================================================
# END FILE
