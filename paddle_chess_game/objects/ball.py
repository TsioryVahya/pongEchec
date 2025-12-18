import pygame
from typing import List, Optional, Tuple

from paddle_chess_game import settings
from .paddle import Paddle
from .chess_piece import ChessPiece


class Ball:
    def __init__(self, x: int, y: int, radius: int = settings.BALL_RADIUS,
                 speed_x: int = settings.BALL_SPEED_X, speed_y: int = settings.BALL_SPEED_Y,
                 color: Tuple[int, int, int] = settings.WHITE):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = speed_x
        self.vy = speed_y
        self.color = color
        self.last_touched_by = None  # Track which player (1 or 2) last touched the ball
        
        # Special Ability State
        self.current_damage = settings.BALL_DAMAGE
        self.is_special = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def reset(self, x: int, y: int, direction: int = 1):
        self.x = x
        self.y = y
        self.vx = abs(self.vx) * direction
        self.vy = settings.BALL_SPEED_Y if self.vy == 0 else self.vy
        self.last_touched_by = None
        self.current_damage = settings.BALL_DAMAGE
        self.is_special = False

    def move(self, bounds: pygame.Rect):
        self.x += self.vx
        self.y += self.vy
        
        # Bounce top/bottom
        if self.y - self.radius <= bounds.top:
            self.y = bounds.top + self.radius
            self.vy *= -1
            # Reset special ability on wall hit
            if self.is_special:
                self.is_special = False
                self.current_damage = settings.BALL_DAMAGE
                
        elif self.y + self.radius >= bounds.bottom:
            self.y = bounds.bottom - self.radius
            self.vy *= -1
            # Reset special ability on wall hit
            if self.is_special:
                self.is_special = False
                self.current_damage = settings.BALL_DAMAGE
        
        # Bounce left/right sides
        if self.x - self.radius <= bounds.left:
            self.x = bounds.left + self.radius
            self.vx *= -1
        elif self.x + self.radius >= bounds.right:
            self.x = bounds.right - self.radius
            self.vx *= -1

    def collide_with_paddle(self, paddle: Paddle):
        if self.rect.colliderect(paddle.rect):
            # Record which player touched the ball
            self.last_touched_by = paddle.owner
            
            # Vertical bounce (for horizontal paddles)
            if self.vy > 0:
                # Ball going down, hit bottom paddle - place ball above paddle
                self.y = paddle.rect.top - self.radius
            else:
                # Ball going up, hit top paddle - place ball below paddle
                self.y = paddle.rect.bottom + self.radius
            self.vy *= -1
            
            # Add horizontal angle based on hit position (adds spin effect)
            offset = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
            self.vx += offset * 1.5  # Reduced spin effect

    def collide_with_pieces(self, pieces: List[ChessPiece]) -> Optional[ChessPiece]:
        hit_piece: Optional[ChessPiece] = None
        ball_rect = self.rect
        
        # Create a copy of the list to avoid issues if we modify it (though we just modify state)
        # We need to check collision with ALL pieces, but only interact with the first one we hit?
        # Actually, if we pierce, we might hit multiple. But usually we hit one at a time per frame.
        
        for piece in pieces:
            if piece.is_alive() and ball_rect.colliderect(piece.rect):
                # Ignore collision with own pieces (friendly fire protection)
                if self.last_touched_by is not None and piece.owner == self.last_touched_by:
                    continue  # Skip collision with own pieces
                
                hit_piece = piece
                
                # Calculate damage to deal
                # If special, we can deal up to current_damage
                # If normal, we deal BALL_DAMAGE (which is current_damage usually)
                
                damage_to_deal = min(piece.life, self.current_damage)
                piece.take_damage(damage_to_deal)
                
                # Reduce current damage capacity if special
                if self.is_special:
                    self.current_damage -= damage_to_deal
                
                is_destroyed = not piece.is_alive()
                
                # PIERCING LOGIC: If special and still has damage, don't bounce
                if self.is_special and self.current_damage > 0:
                    # PIERCING EFFECT
                    # Do not bounce, do not change ownership (keep attacking)
                    # Just continue trajectory to hit pieces behind
                    # Update hit_piece for scoring but don't break the loop
                    if is_destroyed:
                        hit_piece = piece
                    # Continue to next piece without bouncing
                    continue
                else:
                    # BOUNCE EFFECT (Normal ball or ran out of special damage)
                    
                    # Reset special if ran out of damage
                    if self.is_special and self.current_damage <= 0:
                        self.is_special = False
                        self.current_damage = settings.BALL_DAMAGE
                    
                    # Update ownership (deflection)
                    self.last_touched_by = piece.owner
                    
                    # Decide bounce axis: compute overlap
                    overlap_left = ball_rect.right - piece.rect.left
                    overlap_right = piece.rect.right - ball_rect.left
                    overlap_top = ball_rect.bottom - piece.rect.top
                    overlap_bottom = piece.rect.bottom - ball_rect.top
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                    
                    # Handle position correction (unstuck ball)
                    if min_overlap in (overlap_left, overlap_right):
                        # Horizontal collision correction
                        if self.vx > 0:
                            self.x = piece.rect.left - self.radius
                        else:
                            self.x = piece.rect.right + self.radius
                        self.vx *= -1
                    else:
                        # Vertical collision correction
                        if self.vy > 0:
                            self.y = piece.rect.top - self.radius
                        else:
                            self.y = piece.rect.bottom + self.radius
                    
                    # FORCE VERTICAL BOUNCE towards opponent
                    if piece.owner == 1:
                        self.vy = abs(self.vy)
                    elif piece.owner == 2:
                        self.vy = -abs(self.vy)
                        
                    # Stop checking other pieces for this frame (bounce only once)
                    hit_piece = piece
                    break
                    
        return hit_piece

    def direct_to(self, target_x: int, target_y: int, speed: float = None):
        """Direct the ball towards a target position.
        
        Args:
            target_x: X coordinate of the target
            target_y: Y coordinate of the target
            speed: Optional speed magnitude (uses current speed if not specified)
        """
        import math
        
        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return  # Already at target
        
        # Normalize direction
        dx /= distance
        dy /= distance
        
        # Use current speed magnitude if not specified
        if speed is None:
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed == 0:
                speed = max(abs(settings.BALL_SPEED_X), abs(settings.BALL_SPEED_Y))
        
        # Set velocity towards target
        self.vx = dx * speed
        self.vy = dy * speed

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
