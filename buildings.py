from enum import Enum
from game_conf import *

class BuildingNames(Enum):
  FENCE = "Fence"
  GARDEN = "Garden"
  NURSERY = "Nursery"

class Building:
  def __init__(self, name, short):
    self._name = name
    self._short = short

  def _effect(self, game_conf: GameConf):
    print("ruh roh")

  def effect(self):
    return self._effect

  def name(self) -> str:
    return self._name

  def short_name(self) -> str:
    return self._short

class Fence(Building):
  def __init__(self):
    super().__init__(BuildingNames.FENCE, "FNC")

  def _effect(self, game_conf: GameConf):
    cur_base = game_conf.get(GameVars.BASE_PROTECTION)
    game_conf.put(GameVars.BASE_PROTECTION, cur_base + 60)


class BuildingFactory:
  _BUILDING_MAP = dict([
    (BuildingNames.FENCE, Fence)
      ])

  @staticmethod
  def make_building(building_name):
    return BuildingFactory._BUILDING_MAP.get(building_name)()
