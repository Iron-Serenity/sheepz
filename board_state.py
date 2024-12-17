import copy

from buildings import Building, BuildingNames


class BoardState:

  def __init__(self, p_id, game_conf, sheep=0, dogs=0, kettled=0, grist=0, charms=0, pasture_slot=None):
    self._pid = p_id
    self._sheep = sheep
    self._dogs = dogs
    self._kettled = kettled
    self._grist = grist
    self._charms=charms
    self._game_conf = game_conf

    self._pasture_slot: Building = pasture_slot

  def turn_number(self):
    return 1

  def sheep(self):
    return self._sheep

  def dogs(self):
    return self._dogs

  def kettled(self):
    return self._kettled

  def grist(self):
    return self._grist

  def charms(self):
    return self._charms

  def game_conf(self):
    return self._game_conf

  def has_pasture_building(self, building_name: BuildingNames) -> bool:
    return self._pasture_slot is not None and self._pasture_slot.name() == building_name

  def clone_with_new_building(self, pasture_building=None):
    copied_self = copy.deepcopy(self)
    if pasture_building is not None: copied_self._pasture_slot = pasture_building

    return copied_self

  def clone_with_diff(self, sheep=0, dogs=0, kettled=0, grist=0, charms=0, pasture_building=None):
    return BoardState(
      self._pid,
      sheep=self._sheep + sheep,
      dogs=self._dogs + dogs,
      kettled=self._kettled + kettled,
      grist=self._grist + grist,
      charms=self._charms + charms,
      game_conf=self._game_conf,
      pasture_slot=pasture_building if pasture_building is not None else self._pasture_slot)