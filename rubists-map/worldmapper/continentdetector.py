# import the necessary packages
import cv2
import pygame

class ContinentDetector:
  def __init__(self):
    self.continents = {
      'usa': pygame.Rect(0, 0, 291, 200),
      'southAmerica': pygame.Rect(0, 201, 291, 457),
      'europe': pygame.Rect(292, 0, 170, 169),
      'asia': pygame.Rect(462, 0, 319, 240),
      'australia': pygame.Rect(595, 241, 160, 100)
    }

  def detect(self, coords):
    for continent, rect in self.continents.items():
      if rect.collidepoint(coords['x'], coords['y']):
        return continent
    return "japan"
