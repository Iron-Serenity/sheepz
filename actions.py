from board_state import *
import random
from math import *
from utils import *
from buildings import *
class Action:

  def __init__(self, board_state: BoardState):
    self._board_state = board_state
    self._used_charms = False
    self._charms_used = 0

  def can_apply(self):
    return True

  def apply(self):
    return self._board_state.clone_with_diff()

  def calc_charm_use(self):
    return 1 + floor(self._board_state.charms()/2)
      
  def used_charms(self):
    return self._used_charms

  def _print_charm(self):
    print("Your charms short out in futility")
    
  def _print_action(self):
    print("Time passes by under darkening stars.")

  def print_action_report(self):
    if self._used_charms:
      self._print_charm()
    self._print_action()

class CallToFieldsAction(Action):

  def __init__(self, board_state: BoardState):
    super().__init__(board_state)
    self._sheep_found = 0
    self._charms_used = 0
    self._extra_sheep_found = 0

  def apply(self):
    base_sheep_found = 2
    range_found = 3
    rolls = 0
    original_roll = random.randint(2,5)
    max_reroll = 0
    
    if (self._board_state.charms() > 0):
      self._used_charms = True
      self._charms_used = self.calc_charm_use()
      base_sheep_found += self._charms_used
      range_found += self._charms_used
      rolls += self._charms_used
      sheep_find_rerolls = [random.randint(base_sheep_found, base_sheep_found + range_found) for i in range (0,rolls)]
      max_reroll = max(sheep_find_rerolls)
      
    self._sheep_found = max(max_reroll, original_roll)
    
    if self._used_charms:
      self._extra_sheep_found = self._sheep_found - original_roll
      
    
    return self._board_state.clone_with_diff(sheep=self._sheep_found, charms=self._charms_used*-1)

  def _print_action(self):
    print(">> {} new sheep follow your calls, joining your flock.".format(self._sheep_found))

  def _print_charm(self):
      print(">> Your voice warps around the chiming of bone charms, carrying further.")
      print(">> {} of your bone charms expend their magic to draw in {} sheep more than your voice alone.".format(self._charms_used, self._extra_sheep_found))

class HireBreederAction(Action):

  def __init__(self, board_state: BoardState):
    super().__init__(board_state)
    self._sheep_spawned = 0

  def can_apply(self):
    return self._board_state.sheep() >=2
  
  def _gen_spawn_func(self):
    if (self._board_state.charms() > 0):
      self._used_charms = True
      self._charms_used = self.calc_charm_use()
      diminish_factor = .75 - (.05 * self._charms_used)
      dim_func = diminish_returns_func(diminish_factor)
      return lambda x: (x/2) + dim_func(x)

    return lambda x:(x/2)

  def apply(self):
    sheep_after_pay = self._board_state.sheep() - 2
    self._sheep_spawned = floor(self._gen_spawn_func()(sheep_after_pay))

    return self._board_state.clone_with_diff(sheep=(self._sheep_spawned - 2), charms=(self._charms_used * -1))

  def _print_action(self):
    print(">> The breeder visits. 2 sheep vanish into his rucksack.\n" +
          ">> The others pair up, a crimson energy bristling through their wool. {} new sheep join your flock.".format(self._sheep_spawned))

  def _print_charm(self):
    extra_sheep = self._sheep_spawned - floor((self._board_state.sheep() - 2)/2)
    print(">> Some of your sheep circle the bone charms on your pasture. A ewephoric blur ripples through their wool.")
    print(">> The {} bone charms they circled go dark, but you're granted with {} additional sheep during the breeder's visit".format(self._charms_used, extra_sheep))

class HireHuntsmanAction(Action):
  def __init__(self, board_state: BoardState, sheep_paid: int):
    super().__init__(board_state)
    self._sheep_paid = sheep_paid
    self._dogs_bought = 0
    self._extra_dogs = 0
    self._dogs_acquired = 0

  def can_apply(self):
    return 0 <= self._sheep_paid <= self._board_state.sheep()

  def apply(self):
    if (self._board_state.charms() > 0):
      self._used_charms = True
      self._charms_used = self.calc_charm_use()
      dog_rolls = [random.random() for i in range(0,self._used_charms)]
      self._extra_dogs = 1 + len([roll for roll in dog_rolls if roll >= .5])
    self._dogs_bought = floor(self._sheep_paid / 5)
    self._dogs_acquired = self._extra_dogs + self._dogs_bought
    return self._board_state.clone_with_diff(sheep=(-1*self._sheep_paid), dogs=self._dogs_acquired, charms=-self._charms_used, kettled=self._charms_used)

  def _print_charm(self):
    print(">> Some of the new whelps bury your bone charms in quiet graves.")
    print(">> Just before nightfall, {} doggs of shadow and loam arise from beneath to patrol with the others.".format(self._extra_dogs))
    print(">> A quiver in the first star's light congratulates you. The lord of the land grants you favor for each of the {} bone charms buried.".format(self._charms_used))
    
  def _print_action(self):
    print(">> The hunstman visits, {} young doggs trailing at his heel.".format(self._dogs_bought))
    print(">> He whistles shrilly through his scarred fingers.")
    print(">> The doggs begin to roam your farm, while {} of your sheep fall in line behind the huntsman as he leaves.".format(self._sheep_paid))

  def print_action_report(self):
    self._print_action()
    if self._used_charms:
      self._print_charm()

class HirePriestAction(Action):
  def __init__(self, board_state: BoardState, sheep_paid: int):
    super().__init__(board_state)
    self._sheep_paid = sheep_paid
    self._favor_gained = 0
    self._grist_gained = 0

  def can_apply(self):
    return 0 <= self._sheep_paid <= self._board_state.sheep()

  def apply(self):
    self._favor_gained += self._sheep_paid
    self._grist_gained = floor(self._sheep_paid/10)
    return self._board_state.clone_with_diff(sheep=(-1*self._sheep_paid), kettled=self._favor_gained, grist=self._grist_gained)

  def _print_action(self):
    print(">> The priest visits, his crimson vestments fluttering in the wind. He sets up an enormous kettle.")
    print(">> With the flick of their wrist, {} of your sheep crawl towards the kettle and toss themselves inside.".format(self._sheep_paid))
    print(">> The sheep bleat an infernal chorus as they disintegrate.")
    print(">> Chuckling grimly, the priest informs you that you've gained {} favor with the lord of the land.".format(self._favor_gained))
    if (self._grist_gained) > 0:
      print(">> Scraping the bottom of the cauldron, their face lights up with surprise. They hand you {} grist.".format(self._grist_gained))

class HireBoneCarverAction(Action):
  def __init__(self, board_state: BoardState, sheep_paid: int):
    super().__init__(board_state)
    self._sheep_paid = sheep_paid
    self._charms_crafted = 0

  def can_apply(self):
    return 0 < self._sheep_paid <= self._board_state.sheep()

  #TODO: extract to common utils
  def _diminish_func(self, x):
    return (pow((x+1), (1-.5)) - 1) / (1-.5)

  def apply(self):
    self._charms_crafted = 1 + floor(self._diminish_func(self._sheep_paid - 1))
    return self._board_state.clone_with_diff(sheep=(-1*self._sheep_paid), charms=self._charms_crafted)

  def _print_action(self):
    print(">> The bonecarver visits with her jingling bag of tools. With slender fingers she sets about her grisly task.")
    print(">> Come nightfall, {} of your sheep have been transformed into {} cryptic structures of sinew and bone.".format(self._sheep_paid, self._charms_crafted))

class BuilderAction(Action):
  def __init__(self, board_state: BoardState, building_chosen):
    super().__init__(board_state)
    self._building_built = building_chosen

  def can_apply(self):
    return self._board_state.grist() >= 1 and self._board_state.sheep() >= 10

  def apply(self):
    building = BuildingFactory.make_building(self._building_built)
    if self._building_built == BuildingNames.FENCE:
      return self._board_state.clone_with_diff(sheep=-10, grist=-1, pasture_building=building)
    
