import sys
import pygame
from typing import List, Dict, Any

from paddle_chess_game import settings
from paddle_chess_game.objects.paddle import Paddle
from paddle_chess_game.objects.ball import Ball
from paddle_chess_game.objects.chess_piece import ChessPiece
from paddle_chess_game.objects.board import Board
from paddle_chess_game.config_menu import ConfigMenu


class Game:
    def __init__(self, config: Dict[str, Any] = None):
        # pygame.init() and set_mode are handled in main.py
        self.screen = pygame.display.get_surface()
        if self.screen is None:
             pygame.init()
             self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
             pygame.display.set_caption(settings.TITLE)
             
        self.clock = pygame.time.Clock()
        self.bounds = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 40)

        # Default values
        self.game_over = False
        self.winner_side = None
        self.starting_player = 1
        self.is_serving = True
        self.serving_player = 1

        # Apply configuration if provided
        if config:
            self.apply_config(config)
        
        # Board with chess-like layout - initialize first to get board dimensions
        self.board = Board()

        # Position paddles AFTER the pawn rows (in front of pieces to protect them)
        # This means: after row 1 for top paddle, before row (BOARD_ROWS-2) for bottom paddle
        paddle_offset = 25  # Distance from pawn row to paddle
        
        # Top paddle (protects player 1) - positioned AFTER row 1 (pawns)
        paddle_x = self.board.board_left + (self.board.cell_size * settings.BOARD_COLS - settings.PADDLE_WIDTH) // 2
        pawn_row_1_bottom = self.board.board_top + 2 * self.board.cell_size  # After row 1 (pawns)
        self.top_paddle = Paddle(
            x=paddle_x,
            y=pawn_row_1_bottom + paddle_offset,
            color=settings.BLUE,
            owner=1,  # Player 1
        )
        
        # Bottom paddle (protects player 2) - positioned BEFORE row (BOARD_ROWS-2) (pawns)
        pawn_row_bottom_top = self.board.board_top + (settings.BOARD_ROWS - 2) * self.board.cell_size
        self.bottom_paddle = Paddle(
            x=paddle_x,
            y=pawn_row_bottom_top - paddle_offset - settings.PADDLE_HEIGHT,
            color=settings.RED,
            owner=2,  # Player 2
        )
        
        # Create bounds for paddle movement (limited to board width)
        self.paddle_bounds = pygame.Rect(
            self.board.board_left,  # Left edge of board
            0,
            self.board.cell_size * settings.BOARD_COLS,  # Board width
            settings.SCREEN_HEIGHT
        )
        
        # Create bounds for ball movement (limited to board area)
        self.board_bounds = pygame.Rect(
            self.board.board_left,  # Left edge of board
            self.board.board_top,   # Top edge of board
            self.board.cell_size * settings.BOARD_COLS,   # Board width
            self.board.cell_size * settings.BOARD_ROWS    # Board height
        )
        
        self.ball = Ball(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, color=settings.BLACK)

    def apply_config(self, config: Dict[str, Any]):
        """Apply configuration settings to the game."""
        # Apply ball speed (same for both X and Y)
        ball_speed = config.get('ball_speed', max(settings.BALL_SPEED_X, settings.BALL_SPEED_Y))
        settings.BALL_SPEED_X = ball_speed
        settings.BALL_SPEED_Y = ball_speed
        
        # Apply board width (must be even: 2, 4, 6, or 8)
        board_width = config.get('board_width', settings.BOARD_COLS)
        # Ensure it's even
        board_width = board_width if board_width % 2 == 0 else board_width - 1
        settings.BOARD_COLS = max(2, min(8, board_width))
        
        # Apply starting player
        self.starting_player = config.get('starting_player', 1)
        self.serving_player = self.starting_player
        
        # Apply piece lives
        settings.CHESS_PIECES_LIVES['roi'] = config.get('roi_lives', settings.CHESS_PIECES_LIVES['roi'])
        settings.CHESS_PIECES_LIVES['reine'] = config.get('reine_lives', settings.CHESS_PIECES_LIVES['reine'])
        settings.CHESS_PIECES_LIVES['fou'] = config.get('fou_lives', settings.CHESS_PIECES_LIVES['fou'])
        settings.CHESS_PIECES_LIVES['tour'] = config.get('tour_lives', settings.CHESS_PIECES_LIVES['tour'])
        settings.CHESS_PIECES_LIVES['chevalier'] = config.get('chevalier_lives', settings.CHESS_PIECES_LIVES['chevalier'])
        settings.CHESS_PIECES_LIVES['pion'] = config.get('pion_lives', settings.CHESS_PIECES_LIVES['pion'])

    def _setup_pieces(self):
        # Deprecated: kept for backward compatibility; Board now manages pieces
        self.board = Board()

    def reset_round(self, direction: int):
        # Instead of launching immediately, go to serving state
        self.is_serving = True
        # If direction is 1 (down), it means player 1 scored or it's P1 turn? 
        # Actually, usually winner serves, or loser serves. Let's say loser serves.
        # If direction was 1 (ball going down), it means P1 launched it?
        # Let's simplify: reset_round is called when ball goes out (but ball doesn't go out anymore).
        # It's only called at start.
        # But wait, ball bounces off edges now. So reset_round is only for game start?
        # Yes, ball stays in play.
        pass

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Top paddle (player 1): A = left, D = right
        if keys[pygame.K_a]:
            self.top_paddle.move(left=True, bounds=self.paddle_bounds)
        if keys[pygame.K_d]:
            self.top_paddle.move(left=False, bounds=self.paddle_bounds)
        # Bottom paddle (player 2): Left Arrow = left, Right Arrow = right
        if keys[pygame.K_LEFT]:
            self.bottom_paddle.move(left=True, bounds=self.paddle_bounds)
        if keys[pygame.K_RIGHT]:
            self.bottom_paddle.move(left=False, bounds=self.paddle_bounds)
            
        # Handle serving (launch ball)
        if self.is_serving and keys[pygame.K_SPACE]:
            # In local game, anyone can serve if it's their turn
            # In network game, we should filter this in main loop, but here we just execute
            if self.serving_player == 1 and (keys[pygame.K_SPACE]): # P1 serve
                 self._serve_ball()
            elif self.serving_player == 2 and (keys[pygame.K_SPACE]): # P2 serve
                 self._serve_ball()

    def process_remote_input(self, player_id: int, input_data: Dict[str, bool]):
        """Process inputs received from network for the remote player."""
        if not input_data:
            return
            
        if player_id == 1:
            # Remote is Player 1 (Top)
            if input_data.get('left'):
                self.top_paddle.move(left=True, bounds=self.paddle_bounds)
            if input_data.get('right'):
                self.top_paddle.move(left=False, bounds=self.paddle_bounds)
            if input_data.get('space') and self.is_serving and self.serving_player == 1:
                self._serve_ball()
        elif player_id == 2:
            # Remote is Player 2 (Bottom)
            if input_data.get('left'):
                self.bottom_paddle.move(left=True, bounds=self.paddle_bounds)
            if input_data.get('right'):
                self.bottom_paddle.move(left=False, bounds=self.paddle_bounds)
            if input_data.get('space') and self.is_serving and self.serving_player == 2:
                self._serve_ball()

    def _serve_ball(self):
        """Launch the ball from serving state."""
        self.is_serving = False
        # Set initial velocity towards opponent
        if self.serving_player == 1:
            self.ball.vy = abs(settings.BALL_SPEED_Y)  # Shoot down
        else:
            self.ball.vy = -abs(settings.BALL_SPEED_Y)  # Shoot up
        import random
        self.ball.vx = random.choice([-1, 1]) * settings.BALL_SPEED_X * 0.5

    def update(self):
        if self.game_over:
            return
            
        if self.is_serving:
            # Ball sticks to the serving paddle
            if self.serving_player == 1:
                paddle = self.top_paddle
                self.ball.y = paddle.rect.bottom + self.ball.radius + 2
            else:
                paddle = self.bottom_paddle
                self.ball.y = paddle.rect.top - self.ball.radius - 2
            
            # Center horizontally on paddle
            self.ball.x = paddle.rect.centerx
            # Update ball ownership to avoind friendly fire immediately
            self.ball.last_touched_by = self.serving_player
            return

        self.ball.move(self.board_bounds)  # Ball stays within board
        # Paddles collision
        self.ball.collide_with_paddle(self.top_paddle)
        self.ball.collide_with_paddle(self.bottom_paddle)
        # Pieces collision
        hit = self.ball.collide_with_pieces(self.board.pieces)
        if hit and hit.type == "roi" and not hit.is_alive():
            # Winner is the opposite owner
            self.winner_side = 1 if hit.owner == 2 else 2
            self.game_over = True

    def get_game_state(self) -> Dict[str, Any]:
        """Get the current game state as a dictionary (for server to send to client)."""
        pieces_data = []
        for p in self.board.pieces:
            pieces_data.append({
                'x': p.rect.x,
                'y': p.rect.y,
                'type': p.type,
                'owner': p.owner,
                'lives': p.life,
                'is_alive': p.is_alive()
            })
            
        return {
            'ball': {'x': self.ball.x, 'y': self.ball.y, 'vx': self.ball.vx, 'vy': self.ball.vy},
            'top_paddle': {'x': self.top_paddle.rect.x, 'y': self.top_paddle.rect.y},
            'bottom_paddle': {'x': self.bottom_paddle.rect.x, 'y': self.bottom_paddle.rect.y},
            'pieces': pieces_data,
            'game_over': self.game_over,
            'winner_side': self.winner_side,
            'is_serving': self.is_serving,
            'serving_player': self.serving_player
        }

    def set_game_state(self, state: Dict[str, Any]):
        """Update game state from dictionary (for client to receive from server)."""
        # Update ball
        self.ball.x = state['ball']['x']
        self.ball.y = state['ball']['y']
        self.ball.vx = state['ball']['vx']
        self.ball.vy = state['ball']['vy']
        
        # Update paddles
        self.top_paddle.rect.x = state['top_paddle']['x']
        self.top_paddle.rect.y = state['top_paddle']['y']
        self.bottom_paddle.rect.x = state['bottom_paddle']['x']
        self.bottom_paddle.rect.y = state['bottom_paddle']['y']
        
        # Update pieces
        server_pieces = state['pieces']
        # Assuming pieces list order hasn't changed, which is true if we don't remove them from list
        # We just mark them as dead/alive
        if len(server_pieces) == len(self.board.pieces):
            for i, p_data in enumerate(server_pieces):
                piece = self.board.pieces[i]
                piece.life = p_data['lives']
                # We don't need to update x/y for static pieces usually, but let's be safe
                # piece.rect.x = p_data['x']
                # piece.rect.y = p_data['y']
        
        self.game_over = state['game_over']
        self.winner_side = state['winner_side']
        self.is_serving = state['is_serving']
        self.serving_player = state['serving_player']

    def draw_ui(self):
        # Simple texts
        if self.game_over:
            msg = f"{settings.WIN_TEXT} (Gagnant: Joueur {self.winner_side})"
            text = self.big_font.render(msg, True, settings.WHITE)
            hint = self.font.render(settings.RESET_HINT, True, settings.GREY)
            self.screen.blit(text, text.get_rect(center=(settings.SCREEN_WIDTH//2, 40)))
            self.screen.blit(hint, hint.get_rect(center=(settings.SCREEN_WIDTH//2, 70)))

    def draw(self):
        self.screen.fill(settings.WHITE)

        # Board hint background (checkerboard)
        self.board.draw_board_hint(self.screen)
        # Draw paddles, ball, pieces
        self.top_paddle.draw(self.screen)
        self.bottom_paddle.draw(self.screen)
        for p in self.board.pieces:
            if p.is_alive():
                p.draw(self.screen)
        self.ball.draw(self.screen)

        self.draw_ui()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_r and self.game_over:
                    # Reset pieces and state
                    self.__init__()

    def run(self):
        while True:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
