from enum import Enum

class GameVars(Enum):
  BASE_PROTECTION = "base_protection"

class GameConf:

  def __init__(self):
    self._var_map = {}
    
  def get(self, var):
    return self._var_map.get(var)

  def put(self, var, val):
    self._var_map.put(var, val)

  def apply(self, modifier):
    modifier.apply(self)
    

#Should really make a version that clones to new on modification and maintains back-pointers
# But this works for now
class BaseConf(GameConf):
  def __init__(self):
    super().__init__()
    self._var_map = dict([
      (GameVars.BASE_PROTECTION, 20)
    ])
