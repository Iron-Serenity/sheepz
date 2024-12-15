import random
from actions import *
from board_state import *
from calculators.WolfCalculator import WolfCalculator, WolfInfoReporter
from game_conf import *

class TurnPrompter:
  
  SUB_MENUS = [2]
  def __init__(self, board_state):
    self._board_state = board_state

  @staticmethod
  def _try_parse_number(value):
    try:
      return int(value)
    except e:
      print("That's not a number I'm familiar with.")
      return None
    
  def parse_main(self, value):
    parsed = TurnPrompter._try_parse_number(value)
    if parsed is None:
      return None

    match parsed:
      case 1:
        return CallToFieldsAction(self._board_state)
      case 2:
        self._print_score_header(1)
        self._trader_submenu()
        user_input = input("Whatcha doin?  ")
        return self.parse_trade(user_input)
      case 3:
        self._print_score_header(1)
        self._builder_submenu()
        user_input = input("Whatcha doin?  ")
        return self.parse_builder(user_input)
      case _:
        print("I'm afraid I don't know what you mean.")
        return None

  def parse_builder(self, value):
    parsed = TurnPrompter._try_parse_number(value)
    if parsed is None:
      return None

    match parsed:
      case 1:
        self._print_score_header(1)
        self._pasture_submenu()
        user_input = input("Whatcha doin?  ")
        return self.parse_pasture(user_input)
      case _:
        print("I'm afraid I don't know what you mean.")
        return None

  def parse_pasture(self, value):
    parsed = TurnPrompter._try_parse_number(value)
    if parsed is None:
      return None

    match parsed:
      case 1:
        return BuilderAction(self._board_state, BuildingNames.FENCE)
      case 2:
        return BuilderAction(self._board_state, BuildingNames.GARDEN)
      case 3:
        return BuilderAction(self._board_state, BuildingNames.NURSERY)
      case _:
        print("I'm afraid I don't know what you mean.")
        return None

  def parse_trade(self, value):
    parsed = TurnPrompter._try_parse_number(value)
    if parsed is None:
      return None

    match parsed:
      case 1:
        return HireBreederAction(self._board_state)
      case 2:
        raw_pay = input("How many sheep do you wish to pay?  ")
        payment = TurnPrompter._try_parse_number(raw_pay)
        if payment is None:
          return None
        return HireHuntsmanAction(self._board_state, payment)
      case 3:
        raw_pay = input("How many sheep do you wish to sacrifice?  ")
        payment = TurnPrompter._try_parse_number(raw_pay)
        if payment is None:
          return None
        return HirePriestAction(self._board_state, payment)
      case 4:
        raw_pay = input("How many sheep do you wish to sacrifice?  ")
        payment = TurnPrompter._try_parse_number(raw_pay)
        if payment is None:
          return None
        return HireBoneCarverAction(self._board_state, payment)
      case _:
        print("I'm afarid I don't know what you mean.")
        return None
    
  def prompt_user(self, cur_turn_number):
    successful_parse = False
    while not successful_parse:
      self._main_menu(cur_turn_number)
      user_input = input("Whatcha doin?  ")
      action = self.parse_main(user_input)
      if action is not None:
        successful_parse = True

    return action

  def _pasture_submenu(self):
    print("--- Ah yes, your rolling green fields  ---")
    print("--- Sure. They could use a sprucing up ---")
    print("------------------------------------")
    print("--- 1. Build a Fence (More sheep protected) - Cost: 1 grist, 10 sheep")
    print("--- 2. Build a Garden (More sheep gained per call) - Cost: 1 grist, 10 sheep")
    print("--- 3. Build a Nursery (More sheep from breeding) - Cost: 1 grist, 10 sheep")

  def _builder_submenu(self):
    print("--- But where? Location is so very important ---")
    print("------------------------------------------------")
    print("--- 1. Pastures ---")

  def _trader_submenu(self):
    print("--- 1. Breeder - Breed all pairs of sheep - Cost: 2 Sheep.")
    print("--- 2. Huntsman - Will give you a dog for every 5 sheep you pay.")
    print("--- 3. Priest - Sacrifice sheep to earn favor. Large sacrifices will get you grist as well.")
    print("--- 4. Bonecarver - Carves charms to bless your actions from the bones of your sheep.")

  def _print_score_header(self, cur_turn_number):
    print("")
    print("----------TURN-----{:03d}-----------".format(cur_turn_number))
    print("--- SHEEP {:03d}   FAVOR {:03d}   CHARM {:03d} ---".format(self._board_state.sheep(), self._board_state.kettled(), self._board_state.charms()))
    print("--- DOGGS {:03d}   GRIST {:03d}   ????? {:03d} ---".format(self._board_state.dogs(), self._board_state.grist(), 0))
    print("-------------------------------")
    
  def _main_menu(self, cur_turn_number):
    self._print_score_header(cur_turn_number)
    print("--- 1. Call to the fields   ---")
    print("--- 2. Trade in town        ---")
    print("--- 3. Build something      ---")


class Turn:

  def __init__(self, initial_board_state: BoardState, turn_number: int):
    self._initial_board_state = initial_board_state
    self.turn_number = turn_number
    self._final_board_state = None

  def _calc_wolf_culling(self, post_action_board_state, min_percent=.7):
    base_protection = post_action_board_state.game_conf().get(GameVars.BASE_PROTECTION)
    DOG_PROTECT = 15
    total_sheep = post_action_board_state.sheep()
    unprotected = total_sheep - base_protection - (DOG_PROTECT * post_action_board_state.dogs())
    percent_taken = (random.randint(0, 3) * .1) + min_percent
    sheep_taken = percent_taken * max(unprotected, 0)
    
    return int(sheep_taken)

  def _wolves_report(self, culled_number, board_state):
    has_dogs = board_state.dogs() > 0
    if (culled_number == 0):
      if (has_dogs):
        print(">> Your watchful dogs keep the wolves at bay for the evening.")
      else:
        print(">> Your small flock slips beneath the attention of wolves for the evening.")
    else:
      if (has_dogs):
        print(">> Your dogs are spread too thin to protect your growing flock. In the morning your flock is {} sheep fewer.".format(culled_number)) 
      else:
        print(">> Wolves sneak through your sleeping flock. In the morning your flock is {} sheep fewer.".format(culled_number))
    
  def take_turn(self, action: Action):
    result_of_action = action.apply()
    
    print("\n-----THE TOIL BY DAYLIGHT-----")
    action.print_action_report()

    print("\n-----WHAT SLINKS IN THE NIGHT-----")

    wolf_turn_info = WolfCalculator(result_of_action).calc_wolves_hunt()

    sheep_killed = wolf_turn_info.sheep_taken_final
    charms_spent = wolf_turn_info.charms_spent

    WolfInfoReporter.print_report(wolf_turn_info)
    self._wolves_report(sheep_killed, result_of_action)
    post_wolves = result_of_action.clone_with_diff(sheep=-1 * sheep_killed, charms=-1 * charms_spent)
    
    self._final_board_state = post_wolves
    return post_wolves
  
class GameRunner:
  def __init__(self):
    self._turns = 0
    self._player_board = None
    self._conf = None

  def setup(self):
    self._turns = 0;
    self._conf = BaseConf()
    self._player_board = BoardState(1, self._conf, sheep=20)

  def play(self):
    while self._turns < 21:
      cur_turn_number = self._turns + 1
      cur_turn = Turn(self._player_board, cur_turn_number)
      prompter = TurnPrompter(self._player_board)
      action = prompter.prompt_user(cur_turn_number)
      if action.can_apply():
        next_board_state = cur_turn.take_turn(action)
        self._player_board = next_board_state
        self._turns += 1
      else:
        print("Hmmm something seems off there")
    
    print("\n\n---THE DAY HAS ARRIVED---\n")
    print("The day finally arrives and the Lord of the Land throws back the hills like bothersome tassels.")
    print("You achieved {} favor before the end of days!".format(self._player_board.kettled()))

if __name__ == "__main__":
  runner = GameRunner()
  runner.setup()
  runner.play()
