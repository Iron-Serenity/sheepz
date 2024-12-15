from collections import namedtuple
from enum import Enum
from game_conf import *

class BuildingNames(Enum):
  FENCE = "Fence"
  GARDEN = "Garden"
  NURSERY = "Nursery"

BuildingCost = namedtuple("BuildingCost", ["grist", "sheep"])

class Building:
  def __init__(self, name, short, building_cost):
    self._name = name
    self._short = short
    self._cost = building_cost

  def cost(self):
    return self._cost

  def name(self) -> str:
    return self._name

  def short_name(self) -> str:
    return self._short

class Fence(Building):
  def __init__(self):
    super().__init__(BuildingNames.FENCE, "FNC", BuildingCost(1,10))

class Nursery(Building):
  def __init__(self):
    super().__init__(BuildingNames.NURSERY, "NUR", BuildingCost(1,10))

class Garden(Building):
  def __init__(self):
    super().__init__(BuildingNames.GARDEN, "GAR", BuildingCost(1,10))


class BuildingFactory:
  _BUILDING_MAP = dict([
    (BuildingNames.FENCE, Fence),
    (BuildingNames.GARDEN, Garden),
    (BuildingNames.NURSERY, Nursery)
  ])

  @staticmethod
  def make_building(building_name):
    return BuildingFactory._BUILDING_MAP.get(building_name)()
