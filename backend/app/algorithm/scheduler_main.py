import random
from typing import List, Optional, Any
# Assuming the necessary classes have been converted and imported correctly:
from chromosome import Chromosome
from gene import Gene
from time_table import TimeTable
# from utility import Utility
from input_data import InputData 
import copy # Needed for deepClone equivalent

# NOTE: The actual implementation of the Placeholder classes below 
# MUST be replaced with the instantiated objects (InputData, TimeTable) 
# in the final __init__ method for the algorithm to function correctly.

class SchedulerMain:
    """
    Main driver for the Genetic Algorithm timetable scheduler.
    Implements population management (elitism), selection (roulette wheel), 
    crossover (single-point gene swap), and mutation.
    """
    
    # Static variable equivalent in Python (shared across all instances)
    final_son: Optional['Chromosome'] = None
    
    def __init__(self, config_data: InputData):
        """Initializes the GA, loads data, and starts the evolution."""
        
        # Use the actual loaded data and configuration
        self.config = config_data
        # self.utility = Utility() # Assuming Utility is instantiated/used correctly
        
        # Instance attributes
        self.first_list: List['Chromosome'] = []
        self.new_list: List['Chromosome'] = []
        self.first_list_fitness: float = 0.0
        self.new_list_fitness: float = 0.0
        self.population_size: int = 1000
        self.max_generations: int = 100

        print("Timetable scheduling started using Genetic Algorithm.")
        
        # 1. Print input data (Testing purpose)
        # self.utility.print_input_data(self.config)
        
        # 2. Generating slots (Uses the actual TimeTable class)
        # NOTE: TimeTable constructor typically initializes the static TimeTable.slot
        TimeTable(self.config) 
        
        # 3. Printing slots (Testing purpose)
        # self.utility.print_slots(self.config, TimeTable)
        
        # 4. Initialising first generation of chromosomes
        self._initialise_population()
        
        # 5. Generating newer generation of chromosomes
        self._create_new_generations()
    
    # --- Population Management ---

    def _initialise_population(self):
        """Generates the first generation of random chromosomes."""
        
        self.first_list = []
        self.first_list_fitness = 0.0
        
        for i in range(self.population_size):
            # Chromosome constructor requires the config object for data access
            c = Chromosome(self.config) 
            self.first_list.append(c)
            self.first_list_fitness += c.fitness
            
        # Sort the initial list (using the __lt__ method implemented in Chromosome)
        self.first_list.sort(reverse=True)
        # print("----------Initial Generation-----------\n")
        self._print_generation(self.first_list)

    def _create_new_generations(self):
        """Creates new Generations using elitism, selection, crossover, and mutation."""
        
        nogenerations = 0
        
        while nogenerations < self.max_generations:	
            
            self.new_list = []
            self.new_list_fitness = 0.0
            i = 0
            
            # 1. Elitism: first 1/10 chromosomes added as is
            elite_size = min(self.population_size // 10, len(self.first_list))
            for i in range(elite_size):
                elite_chromosome = self.first_list[i].deep_clone()
                self.new_list.append(elite_chromosome)
                self.new_list_fitness += elite_chromosome.fitness

            
            # 2. Generating rest of the population (Selection, Crossover, Mutation)
            while i < self.population_size:
                
                father = self._select_parent_roulette()
                mother = self._select_parent_roulette()
                son = None
        
                # Crossover (using config.crossover_rate)
                if random.random() < self.config.crossover_rate:
                    son = self._crossover(father, mother)	
                else:
                    son = father # If no crossover, father is passed forward
                
                # Mutation
                self._custom_mutation(son)
                
                if son.fitness == 1.0:
                    # print("Selected Chromosome is:-")
                    son.print_chromosome()
                    break # Solution found
                
                self.new_list.append(son)
                self.new_list_fitness += son.get_fitness() # Recalculate fitness before adding
                i += 1
                
            # 3. Check for successful generation (fitness 1.0 found)
            if i < self.population_size:
                
                # print("****************************************************************************************")
                # print(f"\n\nSuitable Timetable has been generated in the {i}th Chromosome of {nogenerations + 2} generation with fitness 1.")
                print("\nGenerated Timetable is:")
                son.print_time_table()
                SchedulerMain.final_son = son
                break
                
            # 4. Preparation for Next Generation
            self.first_list = self.new_list
            # Python's list.sort() is in-place
            self.first_list.sort(reverse=True) 
            
            # print(f"**************************      Generation{nogenerations + 2}      ********************************************\n")
            self._print_generation(self.first_list)
            nogenerations += 1

    # --- Genetic Operations ---

    def _select_parent_roulette(self) -> 'Chromosome':
        """
        Selects a parent using Roulette Wheel Selection only from the best 10% chromosomes.
        """
        elite_size = self.population_size // 10
        
        # Calculate the total fitness of the elite portion
        elite_list = self.first_list[:elite_size]
        elite_fitness_sum = sum(c.fitness for c in elite_list)
        
        if elite_fitness_sum == 0:
             # Fallback: simple random choice if total fitness is zero
             return random.choice(elite_list).deep_clone()

        random_float = random.uniform(0, elite_fitness_sum)
        current_sum = 0.0

        for chromosome in elite_list:
            current_sum += chromosome.fitness
            if current_sum >= random_float:
                return chromosome.deep_clone() 
                
        # Should not be reached, but fallback to the last elite item
        return elite_list[-1].deep_clone()
		
		
    def _custom_mutation(self, c: 'Chromosome'):
        """
        Custom mutation: replaces a random gene (group's schedule) until the 
        chromosome's fitness is no worse than its previous fitness (greedy).
        """
        old_fitness = c.get_fitness()
        geneno = random.randrange(self.config.nostudentgroup)
        
        i = 0
        while True:
            # Create a new random Gene for the selected student group
            # Gene constructor requires group index and config/data
            c.gene[geneno] = Gene(geneno, self.config)
            new_fitness = c.get_fitness()
            
            if new_fitness >= old_fitness:
                break # Accept mutation if fitness improved or stayed the same
            
            i += 1
            if i >= 500000: # Emergency break condition
                break	
		
	
    def _crossover(self, father: 'Chromosome', mother: 'Chromosome') -> 'Chromosome':
        """
        Performs single-point crossover by swapping a random Gene (a single group's schedule) 
        and returns the better resulting child (greedy selection).
        """
        random_index = random.randrange(self.config.nostudentgroup)
        
        # Swap the Gene at the random index between the two parents
        temp = father.gene[random_index].deep_clone()
        father.gene[random_index] = mother.gene[random_index].deep_clone()
        mother.gene[random_index] = temp

        # Calculate fitness for the two new children 
        father.get_fitness()
        mother.get_fitness()
        
        # Return the child with the higher fitness
        if father.fitness > mother.fitness:
            return father
        else:
            return mother
	
    # --- Printing and Utility Methods ---

    # def _print_generation(self, list: List['Chromosome']):
    #     """Prints important details of a generation (top 4, and specific indices)."""
        
    #     # print("Fetching details from this generation...\n")	

    #     # Print only initial 4 chromosomes of sorted list
    #     for i in range(min(4, len(list))):
    #         # print(f"Chromosome no.{i}: {list[i].get_fitness()}")
    #         list[i].print_chromosome()
    #         # print("")
        
    #     index_10_percent = self.population_size // 10
    #     index_20_percent = self.population_size // 5

    #     if index_10_percent + 1 < len(list):
    #         print(f"Chromosome no. {index_10_percent + 1} :{list[index_10_percent + 1].get_fitness()}\n")
        
    #     if index_20_percent + 1 < len(list):
    #         print(f"Chromosome no. {index_20_percent + 1} :{list[index_20_percent + 1].get_fitness()}\n")

    #     if list:
    #         print(f"Most fit chromosome from this generation has fitness = {list[0].get_fitness()}\n")
    
    
    def select_parent_best(self, list: List['Chromosome']) -> 'Chromosome':
        """Selects randomly from the best 100 chromosomes (alternate selection)."""
        random_int = random.randrange(min(100, len(list)))
        return list[random_int].deep_clone()

    def mutation_simple(self, c: 'Chromosome'):
        """Simple mutation: circular shift of the first gene's schedule."""
        # This function relies on inputdata constants which should be accessed via self.config
        total_slots = self.config.daysperweek * self.config.hoursperday
        geneno = random.randrange(self.config.nostudentgroup)
        slot_list = c.gene[geneno].slotno
        
        # Circular shift: move first element to the end
        temp = slot_list[0]
        slot_list[:-1] = slot_list[1:]
        slot_list[-1] = temp
        c.get_fitness() 
    
    def swap_mutation(self, c: 'Chromosome'):
        """Swaps two random slots within a random gene's schedule."""
        total_slots = self.config.daysperweek * self.config.hoursperday
        geneno = random.randrange(self.config.nostudentgroup)
        slot_list = c.gene[geneno].slotno
        
        slotno1 = random.randrange(total_slots)
        slotno2 = random.randrange(total_slots)
        
        # Swap values
        slot_list[slotno1], slot_list[slotno2] = slot_list[slotno2], slot_list[slotno1]
        c.get_fitness() 


if __name__ == "__main__":
    # This block is the execution entry point.
    
    # 1. Load configuration and data
    config_data = InputData("input.txt") # Assuming input.txt is used here
    
    # 2. Run the GA
    SchedulerMain(config_data)