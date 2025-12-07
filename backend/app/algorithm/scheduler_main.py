import random
from typing import List, Optional, Any
import copy 

from app.algorithm.chromosome import Chromosome
from app.algorithm.gene import Gene
from app.algorithm.time_table import TimeTable
from app.algorithm.input_data import InputData 

class SchedulerMain:

    final_son: Optional['Chromosome'] = None
    
    def __init__(self, config_data: InputData):
                
        self.config = config_data
            
        self.first_list: List['Chromosome'] = []
        self.new_list: List['Chromosome'] = []
        self.first_list_fitness: float = 0.0
        self.new_list_fitness: float = 0.0
        self.population_size: int = 1000
        self.max_generations: int = 100

        TimeTable(self.config) 
                
        self._initialise_population()
        
        self._create_new_generations()
    
    def _initialise_population(self):    
        self.first_list = []
        self.first_list_fitness = 0.0
        
        for i in range(self.population_size):
            c = Chromosome(self.config) 
            self.first_list.append(c)
            self.first_list_fitness += c.fitness
    
        self.first_list.sort(reverse=True)    
        self._print_generation(self.first_list)

    def _create_new_generations(self):        
        nogenerations = 0
        while nogenerations < self.max_generations:	
            
            self.new_list = []
            self.new_list_fitness = 0.0
            i = 0
            elite_size = min(self.population_size // 10, len(self.first_list))
            for i in range(elite_size):
                elite_chromosome = self.first_list[i].deep_clone()
                self.new_list.append(elite_chromosome)
                self.new_list_fitness += elite_chromosome.fitness
            while i < self.population_size:
                
                father = self._select_parent_roulette()
                mother = self._select_parent_roulette()
                son = None
                if random.random() < self.config.crossover_rate:
                    son = self._crossover(father, mother)	
                else:
                    son = father 
                
                
                self._custom_mutation(son)
                
                if son.fitness == 1.0:
                    
                    son.print_chromosome()
                    break 
                
                self.new_list.append(son)
                self.new_list_fitness += son.get_fitness() 
                i += 1
            if i < self.population_size:
                son.print_time_table()
                SchedulerMain.final_son = son
                break
                
            self.first_list = self.new_list
            
            self.first_list.sort(reverse=True) 
            
            self._print_generation(self.first_list)
            nogenerations += 1

    def _select_parent_roulette(self) -> 'Chromosome':
        elite_size = self.population_size // 10
        
        elite_list = self.first_list[:elite_size]
        elite_fitness_sum = sum(c.fitness for c in elite_list)
        
        if elite_fitness_sum == 0:
             
             return random.choice(elite_list).deep_clone()

        random_float = random.uniform(0, elite_fitness_sum)
        current_sum = 0.0

        for chromosome in elite_list:
            current_sum += chromosome.fitness
            if current_sum >= random_float:
                return chromosome.deep_clone() 
                
        return elite_list[-1].deep_clone()
		
		
    def _custom_mutation(self, c: 'Chromosome'):
        old_fitness = c.get_fitness()
        geneno = random.randrange(self.config.nostudentgroup)
        i = 0
        while True:
            c.gene[geneno] = Gene(geneno, self.config)
            new_fitness = c.get_fitness()
            
            if new_fitness >= old_fitness:
                break 
            
            i += 1
            if i >= 500000: 
                break	
		
    def _crossover(self, father: 'Chromosome', mother: 'Chromosome') -> 'Chromosome':
        random_index = random.randrange(self.config.nostudentgroup)
        
        
        temp = father.gene[random_index].deep_clone()
        father.gene[random_index] = mother.gene[random_index].deep_clone()
        mother.gene[random_index] = temp

        
        father.get_fitness()
        mother.get_fitness()
        
        
        if father.fitness > mother.fitness:
            return father
        else:
            return mother
	
    def _print_generation(self, list: List['Chromosome']):
        for i in range(min(4, len(list))):
    
            list[i].print_chromosome()
    
        
        index_10_percent = self.population_size // 10
        index_20_percent = self.population_size // 5
    
    def select_parent_best(self, list: List['Chromosome']) -> 'Chromosome':
        random_int = random.randrange(min(100, len(list)))
        return list[random_int].deep_clone()

    def mutation_simple(self, c: 'Chromosome'):
        total_slots = self.config.daysperweek * self.config.hoursperday
        geneno = random.randrange(self.config.nostudentgroup)
        slot_list = c.gene[geneno].slotno
    
        temp = slot_list[0]
        slot_list[:-1] = slot_list[1:]
        slot_list[-1] = temp
        c.get_fitness() 
    
    def swap_mutation(self, c: 'Chromosome'):
        total_slots = self.config.daysperweek * self.config.hoursperday
        geneno = random.randrange(self.config.nostudentgroup)
        slot_list = c.gene[geneno].slotno
        
        slotno1 = random.randrange(total_slots)
        slotno2 = random.randrange(total_slots)
        
        
        slot_list[slotno1], slot_list[slotno2] = slot_list[slotno2], slot_list[slotno1]
        c.get_fitness() 

if __name__ == "__main__":
    config_data = InputData("input.txt") 
    SchedulerMain(config_data)