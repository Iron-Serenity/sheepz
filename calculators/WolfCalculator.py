import random
from collections import namedtuple
from math import floor

from board_state import BoardState
from buildings import BuildingNames
from game_conf import GameVars


WolfCalcInfo = namedtuple('WolfInfo', ['charms_spent', 'sheep_taken_final', 'sheep_taken_initial'])

class WolfCalculator:

  def __init__(self, board_state: BoardState):
    self.board_state = board_state

  def base_protection(self) -> int:
    bonus_protection_from_fence = 60 if self.board_state.has_pasture_building(BuildingNames.FENCE) else 0 
    return self.board_state.game_conf().get(GameVars.BASE_PROTECTION) + bonus_protection_from_fence

  def calc_dog_protection(self) -> int:
    protection_per_dog = 15
    return protection_per_dog * self.board_state.dogs()

  def calculate_protection(self) -> int:
    return self.base_protection() + self.calc_dog_protection()

  def calc_percent_taken(self, min_percent=.7) -> float:
     return  (random.randint(0, 3) * .1) + min_percent

  def calc_wolves_hunt(self):

    protection = self.calculate_protection()
    unprotected_sheep = self.board_state.sheep() - protection
    base_percent_taken = self.calc_percent_taken()

    sheep_taken = int(base_percent_taken * max(unprotected_sheep, 0))

    ret_info = WolfCalcInfo(0, sheep_taken, sheep_taken)

    if sheep_taken > 0 and self.board_state.charms() > 0:
      charms_spent = 1 + floor((self.board_state.charms() - 1) / 2)
      percent_redux = min(.6, charms_spent * .1)
      new_min_percent = .7 - percent_redux
      new_sheep_killed = max(0, unprotected_sheep * self.calc_percent_taken(min_percent=new_min_percent) - 1)
      ret_info = WolfCalcInfo(charms_spent, int(new_sheep_killed), sheep_taken)

    return ret_info

class WolfInfoReporter:
  @staticmethod
  def print_report(wolf_turn_info: WolfCalcInfo):
    if wolf_turn_info.charms_spent > 0:
      print(">> As the wolves gather in the wreathing shadows, your bone charms jangle whispers of protection.")
      print(">> {} of your charms expend their energy reducing the sheep taken from {} to {}.".format(wolf_turn_info.charms_spent,
                                                                                                      wolf_turn_info.sheep_taken_initial,
                                                                                                      wolf_turn_info.sheep_taken_final))
