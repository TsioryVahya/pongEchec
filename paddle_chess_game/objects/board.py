from typing import List
import pygame

from paddle_chess_game import settings
from paddle_chess_game.objects.chess_piece import ChessPiece


BACK_RANK = ["tour", "chevalier", "fou", "reine", "roi", "fou", "chevalier", "tour"]
PAWN_RANK = ["pion"] * 8


class Board:
    """Manage a more chess-like distribution of pieces for both sides.

    This does NOT implement chess rules; it only places static pieces used as obstacles.
    """

    def __init__(self):
        self.pieces: List[ChessPiece] = []
        self.bounds = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self._layout_pieces()

    def _layout_pieces(self):
        """Layout pieces in a standard chess board formation with configurable dimensions.
        
        Each player gets 2 rows:
        - Owner 1 (top): Row 0 = back rank, Row 1 = pawns
        - Owner 2 (bottom): Row (n-2) = pawns, Row (n-1) = back rank
        
        Only the center pieces are placed based on BOARD_COLS:
        - 2 cols: Roi, Reine
        - 4 cols: Fou, Reine, Roi, Fou
        - 6 cols: Chevalier, Fou, Reine, Roi, Fou, Chevalier
        - 8 cols: Tour, Chevalier, Fou, Reine, Roi, Fou, Chevalier, Tour
        """
        cols = settings.BOARD_COLS
        rows = settings.BOARD_ROWS
        
        # Calculate the largest square cell size that fits the screen
        cell_size = min(settings.SCREEN_WIDTH // cols, settings.SCREEN_HEIGHT // rows)
        
        # Store dimensions
        self.cell_size = cell_size
        self.cell_width = cell_size  # Square cells
        self.cell_height = cell_size  # Square cells
        
        # Center the board if there are margins
        self.board_left = (settings.SCREEN_WIDTH - cell_size * cols) // 2
        self.board_top = (settings.SCREEN_HEIGHT - cell_size * rows) // 2
        
        # Determine which pieces to use based on board width
        # Full back rank: ["tour", "chevalier", "fou", "reine", "roi", "fou", "chevalier", "tour"]
        # Take the center pieces only
        full_back_rank = ["tour", "chevalier", "fou", "reine", "roi", "fou", "chevalier", "tour"]
        start_col = (8 - cols) // 2  # Center alignment
        active_back_rank = full_back_rank[start_col:start_col + cols]
        
        # Place pieces for owner 1 (top 2 rows)
        # Row 0: Back rank
        for c in range(cols):
            x = self.board_left + c * cell_size + (cell_size - settings.PIECE_WIDTH) // 2
            y = self.board_top + (cell_size - settings.PIECE_HEIGHT) // 2
            self.pieces.append(ChessPiece(x, y, active_back_rank[c], owner=1))
        
        # Row 1: Pawns
        for c in range(cols):
            x = self.board_left + c * cell_size + (cell_size - settings.PIECE_WIDTH) // 2
            y = self.board_top + cell_size + (cell_size - settings.PIECE_HEIGHT) // 2
            self.pieces.append(ChessPiece(x, y, "pion", owner=1))
        
        # Place pieces for owner 2 (bottom 2 rows)
        # Row (rows-2): Pawns
        for c in range(cols):
            x = self.board_left + c * cell_size + (cell_size - settings.PIECE_WIDTH) // 2
            y = self.board_top + (rows - 2) * cell_size + (cell_size - settings.PIECE_HEIGHT) // 2
            self.pieces.append(ChessPiece(x, y, "pion", owner=2))
        
        # Row (rows-1): Back rank
        for c in range(cols):
            x = self.board_left + c * cell_size + (cell_size - settings.PIECE_WIDTH) // 2
            y = self.board_top + (rows - 1) * cell_size + (cell_size - settings.PIECE_HEIGHT) // 2
            self.pieces.append(ChessPiece(x, y, active_back_rank[c], owner=2))

    def draw_board_hint(self, surface: pygame.Surface):
        """Draw a proper checkerboard pattern with alternating beige and brown squares."""
        if not hasattr(self, 'cell_size'):
            return
        
        cols = settings.BOARD_COLS
        rows = settings.BOARD_ROWS
        
        for row in range(rows):
            for col in range(cols):
                # Alternate colors like a real chessboard
                if (row + col) % 2 == 0:
                    color = settings.BEIGE
                else:
                    color = settings.BROWN
                
                x = self.board_left + col * self.cell_size
                y = self.board_top + row * self.cell_size
                
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, color, rect)
