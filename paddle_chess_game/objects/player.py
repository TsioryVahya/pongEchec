import pygame
from typing import List, Tuple
from paddle_chess_game import settings
from paddle_chess_game.objects.paddle import Paddle
from paddle_chess_game.objects.chess_piece import ChessPiece


class Player:
    """Represents a player in the game with their paddle and pieces."""
    
    def __init__(self, player_id: int, paddle: Paddle, color: Tuple[int, int, int]):
        """
        Initialize a player.
        
        Args:
            player_id: 1 or 2
            paddle: The player's paddle
            color: The player's color (for UI elements)
        """
        self.id = player_id
        self.paddle = paddle
        self.color = color
        self.pieces: List[ChessPiece] = []
        self.score = 0
        
    def add_piece(self, piece: ChessPiece):
        """Add a chess piece to this player's collection."""
        self.pieces.append(piece)
    
    def get_alive_pieces(self) -> List[ChessPiece]:
        """Get all pieces that are still alive."""
        return [p for p in self.pieces if p.is_alive()]
    
    def get_king(self) -> ChessPiece:
        """Get the player's king piece."""
        for piece in self.pieces:
            if piece.type == "roi":
                return piece
        return None
    
    def is_defeated(self) -> bool:
        """Check if the player is defeated (king is dead)."""
        king = self.get_king()
        return king is None or not king.is_alive()
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper, bounds: pygame.Rect):
        """Handle keyboard input for this player."""
        if self.id == 1:
            # Player 1: A = left, D = right
            if keys[pygame.K_a]:
                self.paddle.move(left=True, bounds=bounds)
            if keys[pygame.K_d]:
                self.paddle.move(left=False, bounds=bounds)
        elif self.id == 2:
            # Player 2: Left Arrow = left, Right Arrow = right
            if keys[pygame.K_LEFT]:
                self.paddle.move(left=True, bounds=bounds)
            if keys[pygame.K_RIGHT]:
                self.paddle.move(left=False, bounds=bounds)
    
    def draw(self, surface: pygame.Surface):
        """Draw the player's paddle and pieces."""
        self.paddle.draw(surface)
        for piece in self.pieces:
            if piece.is_alive():
                piece.draw(surface)
    
    def __str__(self):
        return f"Player {self.id} ({len(self.get_alive_pieces())}/{len(self.pieces)} pieces alive)"
