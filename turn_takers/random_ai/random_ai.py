from random import *
from actions import *
from buildings import *
from turn_takers.turn_taker import *
from copy import copy

class RandomAi(TurnTaker):

  ACTIONS = [
    lambda bs: CallToFieldsAction(bs),
    lambda bs: HireBreederAction(bs),
    lambda bs: HireHuntsmanAction(bs, RandomAi._pick_valid_sheep_payment(bs, break_point=5)),
    lambda bs: HirePriestAction(bs, RandomAi._pick_valid_sheep_payment(bs, break_point=10)),
    lambda bs: HireBoneCarverAction(bs, RandomAi._pick_valid_sheep_payment(bs)),
    lambda bs: BuilderAction(bs, BuildingNames.FENCE),
    lambda bs: BuilderAction(bs, BuildingNames.GARDEN),
    lambda bs: BuilderAction(bs, BuildingNames.NURSERY)
  ]
  
  def __init__(self):
    pass

  @staticmethod
  def _valid_variable_payment(budget, break_point=None):
  	step_size = 1
  	if break_point is not None:
  	  step_size = break_point

  	if budget < step_size:
  	  return None # Can't make sensible payment

  	if budget == step_size:
  	  return budget # Can make a payment at exactly a poitn to get something

  	steps_in_budget = floor(budget / step_size)

  	return step_size * randint(1, steps_in_budget)

  @staticmethod
  def _pick_valid_sheep_payment(board_state, break_point=None):
  	return RandomAi._valid_variable_payment(board_state.sheep(), break_point)

  
  def take_turn(self, board_state):
  	possible_actions = copy(RandomAi.ACTIONS)

  	shuffle(possible_actions)

  	valid_action = False
  	
  	while valid_action == False:
  	  chosen_action = possible_actions.pop()
  	  if chosen_action is not None:
  	  	chosen_action = chosen_action(board_state)
  	  	valid_action = chosen_action.can_apply()

  	return chosen_action
  	
