import random
from actions import *
from board_state import *

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

    if (False):
      parsed = False
      self._trader_submenu()
      try:
        parsed = int(input("Whatcha doin?  "))
        successful_parse = True
      except e:
        pass

    return action

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


class Turn:

  def __init__(self, initial_board_state: BoardState, turn_number: int):
    self._initial_board_state = initial_board_state
    self.turn_number = turn_number
    self._final_board_state = None

  def _calc_wolf_culling(self, post_action_board_state, min_percent=.7):
    #TODO: move to constant
    BASE_PROTECT = 20
    DOG_PROTECT = 15
    total_sheep = post_action_board_state.sheep()
    unprotected = total_sheep - BASE_PROTECT - (DOG_PROTECT * post_action_board_state.dogs())
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
    if action.used_charms():
      action.charms_string();
    action.action_string()

    print("\n-----WHAT SLINKS IN THE NIGHT-----")
    sheep_killed = self._calc_wolf_culling(result_of_action)
    charms_spent=0
    if (sheep_killed > 1 and result_of_action.charms() > 0):
      charms_spent = 1 + floor(result_of_action.charms()/4)
      percent_redux = min(.6, charms_spent * .1)
      new_min_percent = .7 - percent_redux
      new_sheep_killed = max(1, self._calc_wolf_culling(result_of_action, min_percent=new_min_percent) - 1)
      print(">> As the wolves gather in the wreathing shadows, your bone charms jangle whispers of protection.")
      print(">> {} of your charms expend their energy reducing the sheep taken from {} to {}.".format(charms_spent, sheep_killed, new_sheep_killed))
      sheep_killed = new_sheep_killed
      
      
    self._wolves_report(sheep_killed, result_of_action)
    post_wolves = result_of_action.clone_with_diff(sheep=-1 * sheep_killed, charms=-1 * charms_spent)
    
    self._final_board_state = post_wolves
    return post_wolves
  
class GameRunner:
  def __init__(self):
    self._turns = 0;
    self._player_board = BoardState(1, sheep=13)

  def setup(self):
    self._turns = 0;

  def play(self):
    while True:
      cur_turn_number = self._turns + 1
      cur_turn = Turn(self._player_board, cur_turn_number)
      prompter = TurnPrompter(self._player_board)
      action = prompter.prompt_user(cur_turn_number)
      next_board_state = cur_turn.take_turn(action)
      self._player_board = next_board_state
      self._turns += 1


if __name__ == "__main__":
  runner = GameRunner()
  runner.setup()
  runner.play()
