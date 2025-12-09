import pygame
from typing import Tuple

from paddle_chess_game import settings


class Paddle:
    def __init__(self, x: int, y: int, width: int = settings.PADDLE_WIDTH, height: int = settings.PADDLE_HEIGHT,
                 color: Tuple[int, int, int] = settings.WHITE, speed: int = settings.PADDLE_SPEED, owner: int = 1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.owner = owner  # 1 for player 1, 2 for player 2

    def move(self, left: bool, bounds: pygame.Rect):
        """Move paddle horizontally (left or right)."""
        if left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        # Clamp to bounds horizontally - ensure paddle stays within screen
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)
