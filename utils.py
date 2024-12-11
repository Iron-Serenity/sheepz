from math import *

def diminish_returns_func(n):
  return lambda x: (pow((x+1), 1-n) -1)/(1-n)
