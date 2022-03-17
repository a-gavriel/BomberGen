from random import randint
from random import random as rand_float

class Stat:
  name : str = ""
  value : int = 0
  max_value : int = 0
  min_value : int = 0
  def __init__(self, name : str, value : int, 
      min_value : int = 1, max_value : int = 99):
    
    self.name = name
    self.max_value = max_value
    self.min_value = min_value
    if value == -1:
      self.value = randint(min_value, max_value)
    else:
      self.value = value

  def randomize_small(self):
    self.value += randint(self.min_value, self.max_value)
    self.value // 2


  def randomize(self):
    self.value = randint(self.min_value, self.max_value)


class Bot:

  fitness : float = 0.0

  def __init__(self):
    self.stats = [
      Stat("shoot_distance", -1),
      Stat("lives", -1, 1, 3),
      Stat("speed", -1),
      Stat("evade", -1),
      Stat("hide", -1),
      Stat("place_bomb1", -1),
      Stat("place_bomb2", -1),
      Stat("heal", -1),
      Stat("shield_strength", -1)
    ]

  def __str__(self):
    s = ""
    for stat_i in self.stats:
      spaces = " " * (20 - len(stat_i.name))
      s += f'{stat_i.name}:{spaces}{stat_i.value}\n'
    return s

  def randomize_stats(self) -> None:
    for stat_ in self.stats:
      stat_.value = randint(stat_.min_value, stat_.max_value)

  @staticmethod
  def create_child(parent1 : 'Bot', parent2 : 'Bot') -> 'Bot':
    new_child = Bot()
    for stat_i, (stat_1, stat_2) in enumerate(zip(parent1.stats, parent2.stats)):
      if randint(0,1):
        new_child.stats[stat_i] = stat_1
      else:
        new_child.stats[stat_i] = stat_2

    return new_child

  
  def mutate_one_small(self):
    """
    Performs a small mutation in a random stat.
    Small mutation:
      stat = (stat + random_value)//2
    """
    stat_i = randint(0, len(self.stats) - 1)
    self.stats[stat_i].randomize_small()

  def mutate_one(self):
    """
    Performs a normal mutation in a random stat.
    Normal mutation:
      stat = random_value
    """
    stat_i = randint(0, len(self.stats) - 1)
    self.stats[stat_i].randomize()


  
  def mutate_many_small(self, mutate_percent = 0.2):
    """
    Performs a small mutation in a <mutate_percent> of the stats.
    Small mutation:
      stat = (stat + random_value)//2
    """
    for stat_ in self.stats:
      if rand_float() < mutate_percent:
        stat_.randomize_small()



  def mutate_many(self, mutate_percent = 0.2):
    """
    Performs a small mutation in a <mutate_percent> of the stats.
    Normal mutation:
      stat = random_value
    """
    for stat_ in self.stats:
      if rand_float() < mutate_percent:
        stat_.randomize()

  def calculate_fitness(self) -> None:
    """
    Calculates the fitness of a Bot
    # TODO: Currently only a random value
    """
    self.fitness = rand_float()


  @staticmethod
  def group_calculate_fitness( Bot_list : list['Bot'] ) -> None:
    """
    Calculate the fitness of a list of Bots
    """
    for bot_ in Bot_list:
      bot_.calculate_fitness()


  @staticmethod
  def select_bots(Bot_list : list['Bot'], new_size : int, pick_percent : float = 0.8) -> list['Bot']:
    """
    Performs a selection of the Bots to pass into the next generation.

    """
    if len(Bot_list) == 0:
      raise Exception('Bot list must not be empty')
    if (len(Bot_list) < new_size) or (new_size <= 0):
      raise Exception('new size must be smaller than len(Bot_list) and more than 0')

    Bot_list.sort(key=lambda x: x.fitness, reverse=True)
    
    new_list = []
    
    if pick_percent >= 1.0:
      pick_percent = rand_float()

    if pick_percent < 0.5:
      pick_percent += 0.5
    
    num_best_to_pick = int(pick_percent * new_size)
    num_worst_to_pick = new_size - num_best_to_pick

    for i in range(0, num_best_to_pick + 1):
      new_list.append(Bot_list[i])
    
    for j in range(-1, (-1*num_worst_to_pick - 1), -1):
      new_list.append(Bot_list[j])

    return new_list



