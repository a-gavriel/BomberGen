from enum import Enum

def rgb(r,g,b):
  return (r,g,b)


class Color(Enum):
  RED = rgb(255,0,0)
  RED_1 = rgb(91,26,26)
  RED_2 = rgb(161,45,45)
  RED_3 = rgb(229,55,55)
  
  GREEN_1 = rgb(26,91,26)
  GREEN_2 = rgb(45,161,45)
  GREEN_3 = rgb(55,229,55)

  BLUE_1 = rgb(26,26,91)
  BLUE_2 = rgb(45,45,161)
  BLUE_3 = rgb(55,55,229)

  PURPLE_1 = rgb(144,43,200)

  WHITE = rgb(255,255,255)

  GREY_HALF = rgb(150,150,150)
  GREY_DARK = rgb(50,50,50)
  