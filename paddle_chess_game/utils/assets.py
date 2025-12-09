import os
import pygame

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def asset_path(*parts: str) -> str:
    return os.path.join(_ASSETS_DIR, *parts)


def load_image(rel_path: str) -> pygame.Surface | None:
    """Load an image relative to the assets dir. Return None if not found or fails.
    Uses convert_alpha() for transparency when possible.
    """
    full_path = asset_path(rel_path)
    if not os.path.exists(full_path):
        return None
    try:
        img = pygame.image.load(full_path)
        return img.convert_alpha()
    except Exception:
        return None
