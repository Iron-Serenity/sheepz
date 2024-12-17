from turn_takers.turn_taker import *
from actions import *
from collections import namedtuple

MenuVals = namedtuple("MenuVals", ['prompt', 'options'])



class MenuParser:
  
  def __init__(self, menu_vals: MenuVals):
  	self._menu_vals = menu_vals

  @staticmethod
  def _try_parse_number(value):
    try:
      return int(value)
    except e:
      print("That's not a number I'm familiar with.")
      return None

  def parse_input(self, value):
  	parsed_val = MenuParser._try_parse_number(value)

  	if parsed_val is None:
  	  return None

  	options = self._menu_vals.options
  	num_opts = len(options)
  	if (0 < parsed_val > num_opts):
  	  return None

  	action_to_invoke = options[parsed_val - 1][1]

  	return action_to_invoke


  def print_prompt(self):
  	print(self._menu_vals.prompt)

  def print_opts(self):
  	options = self._menu_vals.options
  	for i in range(len(options)):
  	  print(f"{i+1} - {options[i][0]}")

  def _print_score(self, board_state):
    print("")
    print("----------TURN-----{:03d}-----------".format(board_state.turn_number()))
    print("--- SHEEP {:03d}   FAVOR {:03d}   CHARM {:03d} ---".format(board_state.sheep(), board_state.kettled(), board_state.charms()))
    print("--- DOGGS {:03d}   GRIST {:03d}   ????? {:03d} ---".format(board_state.dogs(), board_state.grist(), 0))
    print("-------------------------------")

  def get_player_input(self, board_state):
  	self._print_score(board_state)
  	self.print_prompt()
  	self.print_opts()
  	value = input("What would you like to do?  ")
  	parsed_val = self.parse_input(value)
  	if parsed_val is None:
  	  return None
  	return parsed_val(board_state)

def payment_step(prompt, board_state, action):
  p = MenuParser._try_parse_number(input(prompt))
  return action(board_state, p)

bonecarver_action = lambda bs: payment_step("HM?", bs, HireBoneCarverAction)
priest_action = lambda bs: payment_step("HM?", bs, HirePriestAction)
huntsman_action = lambda bs: payment_step("HM?", bs, HireHuntsmanAction)
fields_action = lambda board_state: CallToFieldsAction(board_state)

breeder_action = lambda bs: HireBreederAction(bs)

TRADER_MENU = MenuVals(
	prompt="The townsfolk linger near their darkened doors.",
	options=[
	  ["Breeder", breeder_action],
	  ["Huntsman", huntsman_action],
	  ["Priest", priest_action],
	  ["Bonecarver", bonecarver_action]
	])

trader_menu_action = lambda bs: MenuParser(TRADER_MENU).get_player_input(bs)


build_action_for = lambda building_name: lambda bs: BuilderAction(bs, building_name)

PASTURE_MENU = MenuVals(
	prompt="Sure. What to build there?",
	options=[
	["Fence", build_action_for(BuildingNames.FENCE)],
	["Garden", build_action_for(BuildingNames.GARDEN)],
	["Nursery", build_action_for(BuildingNames.NURSERY)]
	])
pasture_menu = lambda bs: MenuParser(PASTURE_MENU).get_player_input(bs)

LOCATION_MENU = MenuVals(
	prompt="But where?",
	options=[
	["Pasture", pasture_menu]])

build_menu_action = lambda bs: MenuParser(LOCATION_MENU).get_player_input(bs)


MAIN_MENU = MenuVals(
  prompt="",
  options=[
    ["Call to Fields", fields_action],
    ["Trade in town", trader_menu_action],
    ["Build something", build_menu_action]
  ]
	)



class TerminalPlayer(TurnTaker):

  def take_turn(self, board_state):
    return MenuParser(MAIN_MENU).get_player_input(board_state)

  