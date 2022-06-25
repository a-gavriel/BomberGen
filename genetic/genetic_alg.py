from random import randint
from random import random as rand_float
from objects import player, bomb

class Stat:
  name : str = ""
  value : int = 0
  min_value : int = 0
  max_value : int = 0

  def __init__(self, name : str, starting_value : int, 
      minimum_value : int = 1, maximum_value : int = 99):
    """
    Creates a new stat with the given <name>, <starting_value>, 
    <minimum_value> and <maximum_value>. If the <starting_value>
    is set to -1, it will generate a new <starting_value> by
    selecting a random value between <minium_value> and 
    <maximum_value>.

    """

    self.name = name
    self.max_value = maximum_value
    self.min_value = minimum_value
    if starting_value == -1:
      self.value = randint(minimum_value, maximum_value)
    else:
      self.value = starting_value

  def randomize_small(self) -> None:
    """
    Generates a new value using the formula:
    value = (value + random_value)//2
    """
    self.value += randint(self.min_value, self.max_value)
    self.value // 2

    return


  def randomize(self) -> None:
    """
    Generates a new value
    """
    self.value = randint(self.min_value, self.max_value)
    
    return


class AI():


  def __init__(game_matrix : list[list[int]], player_list : list[Player],  bomb_list : list[Bomb]):

    
    
    self.stats = [
      Stat("shoot_distance", -1),
      Stat("speed", -1),
      Stat("action_evade", -1),
      Stat("action_hide", -1),
      Stat("action_place_bomb1", -1),
      Stat("action_place_bomb2", -1),
      #Stat("action_heal", -1),
      Stat("shield_strength", -1)
      
    ]
    


    self.normalized_fitness : float = 0.0
    self.accumulated_fitness : float = 0.0

  def __str__(self) -> str:
    """
    When printing a Bot, it will print each of the stats from it.
    """
    s = ""
    for stat_i in self.stats:
      spaces = " " * (20 - len(stat_i.name))
      s += f'{stat_i.name}:{spaces}{stat_i.value}\n'
    return s


  def randomize_stats(self) -> None:
    """
    Randomizes all the stats from a Bot
    """
    for stat_ in self.stats:
      stat_.value = randint(stat_.min_value, stat_.max_value)

  @staticmethod
  def create_child(parent1 : 'Bot', parent2 : 'Bot') -> 'Bot':
    """
    Creates a child Bot from the two parent bots provided.
    The child will inherit all the atributes from the parents.
    Each atribute will be picked at random from whom to 
    inherit it from.
    
    """
    new_child = parent1
    for stat_i, (stat_1, stat_2) in enumerate(zip(parent1.stats, parent2.stats)):
      if randint(0,1):
        #new_child.stats[stat_i] = stat_1
        pass #new_child already has parent1 stat
      else:
        new_child.stats[stat_i] = stat_2

    return new_child

  
  def mutate_one_small(self) -> None:
    """
    Performs a small mutation in a random stat.
    Small mutation:
      stat = (stat + random_value)//2
    """
    stat_i = randint(0, len(self.stats) - 1)
    self.stats[stat_i].randomize_small()

    return

  def mutate_one(self) -> None:
    """
    Performs a normal mutation in a random stat.
    Normal mutation:
      stat = random_value
    """
    stat_i = randint(0, len(self.stats) - 1)
    self.stats[stat_i].randomize()

    return


  
  def mutate_many_small(self, mutate_percent = 0.2) -> None:
    """
    Performs a small mutation in a <mutate_percent> of the stats.
    Small mutation:
      stat = (stat + random_value)//2
    """
    for stat_ in self.stats:
      if rand_float() < mutate_percent:
        stat_.randomize_small()
    
    return



  def mutate_many(self, mutate_percent = 0.2) -> None:
    """
    Performs a small mutation in a <mutate_percent> of the stats.
    Normal mutation:
      stat = random_value
    """
    for stat_ in self.stats:
      if rand_float() < mutate_percent:
        stat_.randomize()

    return 

  def calculate_fitness(self) -> None:
    """
    Calculates the fitness of a Bot
    # TODO: Currently only a random value
    """
    self.fitness = rand_float()

    return


  @staticmethod
  def group_calculate_fitness( Bot_list : list['Bot'] ) -> None:
    """
    Calculate the fitness of a list of Bots
    """
    for bot_ in Bot_list:
      bot_.calculate_fitness()


  @staticmethod
  def select_bots_m1(Bot_list : list['Bot'], new_size : int, pick_percent : float = 0.8) -> list['Bot']:
    """
    Sorts the <Bot_list> and performs a selection of the Bots 
    to pass into the next generation. 
    
    <new_size> defines the number of Bots to pass into the 
    next generation.

    <pick_percent> defines the ratio of how many Bots will be 
    selected from the best ones (based on fitness), the remaining
    will be taken from the worst Bots.

    """
    if len(Bot_list) == 0:
      raise Exception('<Bot list> must not be empty')
    if (len(Bot_list) <= new_size):
      raise Exception('<new_size> must be smaller than len(Bot_list)')
    if  (new_size <= 0):
      raise Exception('<new_size> must be more than 0')

    Bot_list.sort(key=lambda x: x.fitness, reverse=True)
    
    new_list : list['Bot'] = []
    
    if not(0.5 < pick_percent < 1.0):
      raise Exception('<pick_percent> must be between 0.5 and 1')
    
    num_best_to_pick = int(pick_percent * new_size)
    num_worst_to_pick = new_size - num_best_to_pick

    for i in range(0, num_best_to_pick + 1):
      new_list.append(Bot_list[i])
    
    for j in range(-1, (-1*num_worst_to_pick - 1), -1):
      new_list.append(Bot_list[j])

    return new_list



