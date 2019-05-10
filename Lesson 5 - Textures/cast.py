import pygame
from math import pi, cos, sin, floor


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)


wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')
wall4 = pygame.image.load('./wall4.png')
wall5 = pygame.image.load('./wall5.png')


textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
}

class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "a": pi/3,
      "fov": pi/3
    }
    self.map = []
    # self.clear()

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 50):
      for cy in range(y, y + 50):
        tx = int((cx - x)*128 / 50)
        ty = int((cy - y)*128 / 50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)

      i = int(x/50)
      j = int(y/50)

      if self.map[j][i] != ' ':
        hitx = x - i*50
        hity = y - j*50

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / 50)

        return d, self.map[j][i], tx

      self.point(int(x), int(y), (255, 255, 255))

      d += 1

  def draw_stake(self, x, h, texture, tx):
    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      ty = int(((y - start)*128)/(end - start))
      c = texture.get_at((tx, ty))
      self.point(x, y, c)


  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, textures[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(0, 500):
      a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
      d, c, tx = self.cast_ray(a)
      x = 500 + i
      h = 500/(d*cos(a-self.player["a"])) * 70
      self.draw_stake(x, h, textures[c], tx)

pygame.init()
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF|pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')

c = 0
while True:
  screen.fill((113, 113, 113))
  r.render()

  for e in pygame.event.get():
    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
      exit(0)
    if e.type == pygame.KEYDOWN:
      if e.key == pygame.K_a:
        r.player["a"] -= pi/10
      elif e.key == pygame.K_d:
        r.player["a"] += pi/10

      elif e.key == pygame.K_RIGHT:
        r.player["x"] += 10
      elif e.key == pygame.K_LEFT:
        r.player["x"] -= 10
      elif e.key == pygame.K_UP:
        r.player["y"] += 10
      elif e.key == pygame.K_DOWN:
        r.player["y"] -= 10

      if e.key == pygame.K_f:
        if screen.get_flags() and pygame.FULLSCREEN:
            pygame.display.set_mode((1000, 500))
        else:
            pygame.display.set_mode((1000, 500), pygame.FULLSCREEN)

  pygame.display.flip()
