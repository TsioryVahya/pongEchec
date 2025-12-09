import pygame
from typing import Tuple

from paddle_chess_game import settings
from paddle_chess_game.utils.assets import load_image


TYPE_COLORS = {
    "roi": settings.YELLOW,
    "reine": settings.BLUE,
    "tour": settings.GREY,
    "fou": settings.GREEN,
    "chevalier": (186, 85, 211),
    "pion": settings.RED,
}


class ChessPiece:
    def __init__(self, x: int, y: int, piece_type: str, owner: int):
        """
        owner: 1 or 2 to indicate side (left/right). Could be used for layout and win condition attribution.
        """
        self.type = piece_type
        self.owner = owner
        self.max_life = settings.CHESS_PIECES_LIVES.get(piece_type, 1)
        self.life = self.max_life
        self.rect = pygame.Rect(x, y, settings.PIECE_WIDTH, settings.PIECE_HEIGHT)
        self.color = TYPE_COLORS.get(piece_type, settings.WHITE)
        # Try load image: priority type_owner.png then type.png
        self.image: pygame.Surface | None = None
        # Preference: assets/blanc|noir/<type>.png depending on owner
        owner_dir = "blanc" if self.owner == 1 else "noir"
        img = (
            load_image(f"{owner_dir}/{self.type}.png")
            or load_image(f"pieces/{self.type}_{self.owner}.png")
            or load_image(f"pieces/{self.type}.png")
        )
        if img is not None:
            # Scale to rect size
            self.image = pygame.transform.smoothscale(img, (self.rect.width, self.rect.height))

    def is_alive(self) -> bool:
        return self.life > 0

    def take_damage(self, amount: int = 1):
        self.life = max(0, self.life - amount)

    def draw(self, surface: pygame.Surface):
        # Piece body or image
        if self.image is not None:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        # Life bar background
        bar_margin = 2
        bg_rect = pygame.Rect(self.rect.x, self.rect.y - 8, self.rect.width, 6)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect, border_radius=3)
        # Life bar foreground
        if self.max_life > 0:
            ratio = self.life / self.max_life
        else:
            ratio = 0
        fg_width = int(self.rect.width * ratio)
        fg_rect = pygame.Rect(self.rect.x, self.rect.y - 8, fg_width, 6)
        pygame.draw.rect(surface, settings.RED if ratio < 0.34 else settings.GREEN, fg_rect, border_radius=3)
