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
import matplotlib.pyplot as plt

# ANALYSIS FUNCTIONS __________________________________________________________
# FUNCTION: anRabToPlant ------------------------------------------------------
def anRabToPlant():
    rabbits = [1,2,3,4,5,6,7]
    output = []
    
    for k in range(len(rabbits)):
        # grab value for restoring value
        hold = const.RABBITS_PER_BURROW
        
        #Parameters passed
        const.RABBITS_PER_BURROW = rabbits[k] # must be less than 9
        
        eatenPlants = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()           #Initialize Ecosystem
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            eatenPlants.append(eco.plantsEaten)
            
        # restore value
        const.RABBITS_PER_BURROW = hold
        
        output.append(sum(eatenPlants) / len(eatenPlants))

    plt.plot(rabbits, output)
    plt.xlabel("Rabbits per Burrow")
    plt.ylabel("Grass Eaten")
    plt.title("Rabbit population v. Grass Consumption")
    plt.show()

# FUNCTION: anLakeToRab -------------------------------------------------------    
def anLakeToAnimals():
    lakeSpread = [1,2,3,4,5,6,7]
    output1 = []
    output2 = []
    
    for k in range(len(lakeSpread)):
        hold = const.LAKE_SPREAD # grab value for restoring value
        
        const.LAKE_SPREAD = lakeSpread[k]
        
        deadHerbi = []
        deadCarni = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            deadHerbi.append(eco.herbiDied)
            deadCarni.append(eco.carniDied)
            
        const.LAKE_SPREAD = hold # restore value
        
        output1.append(sum(deadHerbi) / len(deadHerbi))
        output2.append(sum(deadCarni) / len(deadCarni))
    
    plt.plot(lakeSpread, output1, label='Herbivores')
    plt.plot(lakeSpread, output2, label='Carnivores')
    plt.xlabel("Lake Size Multiplyer")
    plt.ylabel("Animals Dead")
    plt.title("Lake Size v. Animal Deaths")
    plt.legend()
    plt.show()

# FUNCTION: anDissipationtoRab ------------------------------------------------    
def anDissipationtoRab():
    scentFade = [0.5, 0.6, 0.7, 0.8, 0.9]
    output = []
    
    for k in range(len(scentFade)):
        hold = const.DISSIPATION_RATE # grab value for restoring value
        
        const.DISSIPATION_RATE = scentFade[k]
        
        eatenRabbits = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek() 
            eatenRabbits.append(eco.animalsDeath[4])
        
        output.append(sum(eatenRabbits) / len(eatenRabbits))
        
        const.DISSIPATION_RATE = hold # restore value
    
    plt.plot(scentFade, output)
    plt.xlabel("Scent Trail Fade Percent")
    plt.ylabel("Animals Eaten")
    plt.title("Scent Dissipation v. Animals Consumption")
    plt.show()

# FUNCTION: anFoxToRabAndPlant ------------------------------------------------   
def anFoxToRabAndPlant():
    foxes = [1,2,3,4,5,6,7]
    output1 = []
    output2 = []
    
    for k in range(len(foxes)):
        hold = const.NUM_FOXES # grab value for restoring value
        
        const.NUM_FOXES = foxes[k]
        eatenRabbits = []
        eatenPlants = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            eatenRabbits.append(eco.animalsDeath[4])
            eatenPlants.append(eco.plantsEaten)
            
        output1.append(sum(eatenRabbits) / len(eatenRabbits))
        output2.append(sum(eatenPlants) / len(eatenPlants))
        
        const.NUM_FOXES = hold # restore value
        
    plt.plot(foxes, output1)
    plt.xlabel("Number of Inital Foxes")
    plt.ylabel("Number Animals Eaten")
    plt.title("Initial Foxes v. Animals Consumption")
    plt.show()   
    
    plt.plot(foxes, output2)
    plt.xlabel("Number of Initial Foxes")
    plt.ylabel("Number Plants Eaten")
    plt.title("Initial Foxes v. Plant Consumption")
    plt.show()   
 
# FUNCTION: anPondsToAnimals --------------------------------------------------   
def anPondsToAnimals():
    temp = const.MIN_MOISTURE
    const.MIN_MOISTURE = 0
    hold = const.NUM_PONDS # grab value for restoring value
    
    ponds = [0,1,2,3,4,5,6]
    output1 = []
    output2 = []
    output3 = []
    
    for k in range(len(ponds)):
        const.NUM_PONDS = ponds[k]
        
        deadHerbi = []
        deadCarni = []
        deadPlants = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            deadHerbi.append(eco.herbiDied)
            deadCarni.append(eco.carniDied)
            deadPlants.append(eco.plantsDied)
        
        output1.append(sum(deadHerbi) / len(deadHerbi))
        output2.append(sum(deadCarni) / len(deadCarni))
        output3.append(sum(deadPlants) / len(deadPlants))
    
    plt.plot(ponds, output1, label='Herbivores')
    plt.plot(ponds, output2, label='Carnivores')
    plt.xlabel("Number of Ponds")
    plt.ylabel("Animals Dead")
    plt.title("Pond Count v. Animal Deaths")
    plt.legend()
    plt.show()
    
    plt.plot(ponds, output3)
    plt.xlabel("Number of Ponds")
    plt.ylabel("Plants Dead")
    plt.title("Pond Count v. Plant Deaths")
    plt.show()
    
    const.NUM_PONDS = hold # restore value
    const.MIN_MOISTURE = temp 
 
# FUNCTION: anFoxStepToRab -------------------------------------------------------- 
def anFoxStepToRab():
    hold = const.EXTRA_FOX_STEPS        # grab value for restoring value
    
    foxsteps = [1,2,3,4,5]
    output = []
    
    for k in range(len(foxsteps)):
        const.EXTRA_FOX_STEPS = foxsteps[k]
        eatenRabbits = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            eatenRabbits.append(eco.animalsDeath[4])
            
        output.append(sum(eatenRabbits) / len(eatenRabbits))
        
    
    plt.plot(foxsteps, output)
    plt.xlabel("Number of Extra Fox Moves per Hour")
    plt.ylabel("Number Animals Eaten")
    plt.title("Extra Fox Movement v. Animals Consumption")
    plt.show()  
    
    const.EXTRA_FOX_STEPS = hold
 
# FUNCTION: anEnergyToAnimals -------------------------------------------------
def anWaterCostToDessicate():
    """
        enMove = Energy cost moving in water
        enWait = Energy cost waiting in water
    """        
    hold = const.WATER_MOVE_FACTOR      # grab value for restoring value

    waterMove = [2,4,6,8,10]
    output = []
    
    for k in range(len(waterMove)):
        const.WATER_MOVE_FACTOR = waterMove[k]
        
        numDessicate = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            numDessicate.append(eco.animalDeath[1])
        
        output.append(sum(numDessicate) / len(numDessicate))
    
    plt.plot(waterMove, output)
    plt.xlabel("Water Move Cost Factor")
    plt.ylabel("Animals Dessicated")
    plt.title("Water Move Cost v. Animal Dessicated")
    plt.show()
    
    const.WATER_MOVE_FACTOR = hold # restore value

# FUNCTION: anEnergyToAnimals -------------------------------------------------
def anEnergyCostToStarve():
    """
        enMove = Energy Cost Moving
    """
    hold = const.ENERGY_MOVE_FACTOR         # grab value for restoring value
    
    energyMove = [2,4,6,8,10]
    output = []
    
    for k in range(len(energyMove)):
        const.ENERGY_MOVE_FACTOR = energyMove[k]
        
        numStarve = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            numStarve.append(eco.animalDeath[0])
        
        output.append(sum(numStarve) / len(numStarve))
    
    plt.plot(energyMove, output)
    plt.xlabel("Energy Move Cost Factor")
    plt.ylabel("Animals Starved")
    plt.title("Energy Move Cost v. Animal Starved")
    plt.show()
    
    const.ENERGY_MOVE_FACTOR = hold         # restore value
 
# FUNCTION: anHungerToStarve --------------------------------------------------
def anHungerToStarve():
    hold = const.HUNGRY_PERCENT         # grab value for restoring value
    
    hunger = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    output = []
    
    for k in range(len(hunger)):
        const.HUNGRY_PERCENT = hunger[k]
        
        numStarve = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            numStarve.append(eco.animalDeath[0])
        
        output.append(sum(numStarve) / len(numStarve))
    
    plt.plot(hunger, output)
    plt.xlabel("Animal Hungry Threashold Percent")
    plt.ylabel("Animals Starved")
    plt.title("Hungry Threashold v. Animal Starved")
    plt.show()
    
    const.HUNGRY_PERCENT = hold      # restore value
    
# FUNCTION: anThirstToDessicate -----------------------------------------------  
def anThirstToDessicate():
    hold = const.THIRSTY_PERCENT         # grab value for restoring value
    
    thirst = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
    output = []
    
    for k in range(len(thirst)):
        const.THIRSTY_PERCENT = thirst[k]
        
        numDessicate = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            numDessicate.append(eco.animalDeath[1])
        
        output.append(sum(numDessicate) / len(numDessicate))
    
    plt.plot(thirst, output)
    plt.xlabel("Animal Thirst Threashold Percent")
    plt.ylabel("Animals Dessicated")
    plt.title("Thirst Threashold v. Animal Dessicated")
    plt.show()
    
    const.THIRSTY_PERCENT = hold      # restore value
    
# FUNCTION: anPlantChanceToAnimals --------------------------------------------    
def anPlantChanceToAnimals():
    hold = const.PLANT_CHANCE         # grab value for restoring value
    
    plantChance = [0.2, 0.4, 0.6, 0.8, 1.0]
    output1 = []
    output2 = []
    
    for k in range(len(plantChance)):
        const.PLANT_CHANCE = plantChance[k]
        
        deadHerbi = []
        deadCarni = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            deadHerbi.append(eco.herbiDied)
            deadCarni.append(eco.carniDied)
        
        output1.append(sum(deadHerbi) / len(deadHerbi))
        output2.append(sum(deadCarni) / len(deadCarni))
    
    plt.plot(plantChance, output1, label='Herbivores')
    plt.plot(plantChance, output2, label='Carnivores')
    plt.xlabel("Plant Initialization Chance")
    plt.ylabel("Animals Dead")
    plt.title("Plant Chances v. Animal Deaths")
    plt.legend()
    plt.show()
    
    const.PLANT_CHANCE = hold      # restore value
    
# FUNCTION: anPlantChanceToAnimals --------------------------------------------  
def anPlantUnitsToDeaths():
    hold = const.PLANT_UNITS_TO_EAT         # grab value for restoring value
    
    plantUnits = [1, 2, 3, 4, 5]
    output1 = []
    output2 = []
    output3 = []
    
    for k in range(len(plantUnits)):
        const.PLANT_UNITS_TO_EAT = plantUnits[k]
        
        deadHerbi = []
        deadCarni = []
        deadPlants = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            deadHerbi.append(eco.herbiDied)
            deadCarni.append(eco.carniDied)
            deadPlants.append(eco.plantsEaten)
        
        output1.append(sum(deadHerbi) / len(deadHerbi))
        output2.append(sum(deadCarni) / len(deadCarni))
        output3.append(sum(deadPlants) / len(deadPlants))
    
    plt.plot(plantUnits, output1, label='Herbivores')
    plt.plot(plantUnits, output2, label='Carnivores')
    plt.xlabel("Units of Plant Eaten at A Time")
    plt.ylabel("Animals Dead")
    plt.title("Plant Units v. Animal Deaths")
    plt.legend()
    plt.show()
    
    plt.plot(plantUnits, output3)
    plt.xlabel("Units of Plant Eaten at A Time")
    plt.ylabel("Plants Dead")
    plt.title("Plant Units v. Plant Deaths")
    plt.show()
    
    const.PLANT_UNITS_TO_EAT = hold    # restore value
    
# FUNCTION: anPlantStatsToAnimals ---------------------------------------------  
def anPlantWaterToNumDrinks():
    hold = const.FLORA_WATER_PERCENT         # grab value for restoring value
    
    floraWater = [0.0, 0.025, 0.05, 0.075, 0.1]
    output = []
    
    for k in range(len(floraWater)):
        const.FLORA_WATER_PERCENT = floraWater[k]
        
        drinks = []
        
        for j in range(const.NUM_SIMS):
            eco = sim.EcoSystem()
            for i in range(const.NUM_WEEKS):
                eco.runAWeek()
            drinks.append(eco.timesDrunk)
        
        output.append(sum(drinks) / len(drinks))
    
    plt.plot(floraWater, output)
    plt.xlabel("Plant Water Consumed Percent")
    plt.ylabel("Times Fauna Drunk")
    plt.title("Plant Water Percent v. Times Drunk")
    plt.show()
    
    const.FLORA_WATER_PERCENT = hold      # restore value

# PROGRAM GLOBALS _____________________________________________________________
# Not User Modifiable
    
# PROGRAM SCRIPT ______________________________________________________________
# Driver code for program
print("# Simulations:", const.NUM_SIMS)
print("# Days Per Sim:", const.NUM_WEEKS * const.DAYS_PER_WEEK)

#anRabToPlant()             # DONE
#anFoxToRabAndPlant()       # DONE
#anFoxStepToRab()           # DONE    
#anDissipationtoRab()       # DONE

#anLakeToAnimals()          # DONE
anPondsToAnimals()          # DONE

anEnergyCostToStarve()
anHungerToStarve()

anWaterCostToDessicate()    
anThirstToDessicate()       

anPlantChanceToAnimals()    
anPlantUnitsToDeaths()     # DONE
#anPlantWaterToNumDrinks()  # DONE

  
#==============================================================================
# END FILE
