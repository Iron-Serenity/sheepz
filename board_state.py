class BoardState:

  def __init__(self, p_id, sheep=0, dogs=0, kettled=0, grist=0, charms=0):
    self._pid = p_id
    self._sheep = sheep
    self._dogs = dogs
    self._kettled = kettled
    self._grist = grist
    self._charms=charms

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

  def clone_with_diff(self, sheep=0, dogs=0, kettled=0, grist=0, charms=0):
    return BoardState(
      self._pid,
      sheep=self._sheep + sheep,
      dogs=self._dogs + dogs,
      kettled=self._kettled + kettled,
      grist=self._grist + grist,
      charms=self._charms + charms)
