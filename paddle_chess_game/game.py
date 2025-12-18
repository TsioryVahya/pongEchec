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
        settings.BALL_DAMAGE = config.get('ball_damage', settings.BALL_DAMAGE)
        
        # Apply board width (must be even: 2, 4, 6, or 8)
        board_width = config.get('board_width', settings.BOARD_COLS)
        # Ensure it's even
        board_width = board_width if board_width % 2 == 0 else board_width - 1
        settings.BOARD_COLS = max(2, min(8, board_width))
        
        # Apply starting player
        self.starting_player = config.get('starting_player', 1)
        self.serving_player = self.starting_player
        
        # Service aiming
        self.serve_angle = 0.0 # Degrees, 0 is vertical
        self.serve_angle_direction = 1 # 1 (right) or -1 (left)
        self.serve_angle_speed = 2.0 # Degrees per frame
        
        # Scores
        self.score_p1 = 0
        self.score_p2 = 0
        
        # Special Ability Bar (Shared)
        self.special_bar = 0
        self.special_bar_max = settings.SPECIAL_BAR_MAX
        self.special_ball_damage = settings.SPECIAL_BALL_DAMAGE
        self.special_just_activated = False  # Flag to reset bar on first piece hit
        
        # Pause state
        self.paused = False
        
        # Apply piece lives
        settings.CHESS_PIECES_LIVES['roi'] = config.get('roi_lives', settings.CHESS_PIECES_LIVES['roi'])
        settings.CHESS_PIECES_LIVES['reine'] = config.get('reine_lives', settings.CHESS_PIECES_LIVES['reine'])
        settings.CHESS_PIECES_LIVES['fou'] = config.get('fou_lives', settings.CHESS_PIECES_LIVES['fou'])
        settings.CHESS_PIECES_LIVES['tour'] = config.get('tour_lives', settings.CHESS_PIECES_LIVES['tour'])
        settings.CHESS_PIECES_LIVES['chevalier'] = config.get('chevalier_lives', settings.CHESS_PIECES_LIVES['chevalier'])
        settings.CHESS_PIECES_LIVES['pion'] = config.get('pion_lives', settings.CHESS_PIECES_LIVES['pion'])

        # Apply piece points
        settings.PIECE_VALUES['roi'] = config.get('roi_points', settings.PIECE_VALUES['roi'])
        settings.PIECE_VALUES['reine'] = config.get('reine_points', settings.PIECE_VALUES['reine'])
        settings.PIECE_VALUES['fou'] = config.get('fou_points', settings.PIECE_VALUES['fou'])
        settings.PIECE_VALUES['tour'] = config.get('tour_points', settings.PIECE_VALUES['tour'])
        settings.PIECE_VALUES['chevalier'] = config.get('chevalier_points', settings.PIECE_VALUES['chevalier'])
        settings.PIECE_VALUES['pion'] = config.get('pion_points', settings.PIECE_VALUES['pion'])
        
        # Apply special ability settings
        self.special_bar_max = config.get('special_bar_max', settings.SPECIAL_BAR_MAX)
        self.special_ball_damage = config.get('special_ball_damage', settings.SPECIAL_BALL_DAMAGE)

    def _setup_pieces(self):
        # Deprecated: kept for backward compatibility; Board now manages pieces
        self.board = Board()

    def reset_round(self, direction: int):
        # Instead of launching immediately, go to serving state
        self.is_serving = True
        self.serve_angle = 0.0
        pass

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Top paddle (player 1): A = left, D = right
        if keys[pygame.K_q]:
            self.top_paddle.move(left=True, bounds=self.paddle_bounds)
        if keys[pygame.K_d]:
            self.top_paddle.move(left=False, bounds=self.paddle_bounds)
        # Bottom paddle (player 2): Left Arrow = left, Right Arrow = right
        if keys[pygame.K_LEFT]:
            self.bottom_paddle.move(left=True, bounds=self.paddle_bounds)
        if keys[pygame.K_RIGHT]:
            self.bottom_paddle.move(left=False, bounds=self.paddle_bounds)
            
        # Handle serving aiming
        if self.is_serving:
            aim_speed = 2.0
            
            # Player 1 Aiming (W/S)
            if self.serving_player == 1:
                if keys[pygame.K_z]: # Aim Left (relative to shooting down) -> actually angle negative
                    self.serve_angle = max(-45, self.serve_angle - aim_speed)
                if keys[pygame.K_s]: # Aim Right -> angle positive
                    self.serve_angle = min(45, self.serve_angle + aim_speed)
                # Also allow Up/Down if Host uses arrows
                if keys[pygame.K_UP]:
                     self.serve_angle = max(-45, self.serve_angle - aim_speed)
                if keys[pygame.K_DOWN]:
                     self.serve_angle = min(45, self.serve_angle + aim_speed)

            # Player 2 Aiming (Up/Down)
            elif self.serving_player == 2:
                if keys[pygame.K_UP]: # Aim Left (relative to shooting up) -> angle positive?
                    # Shooting up: positive angle is Right. 
                    # Let's say UP increases angle (Right), DOWN decreases (Left)
                    # Or visually: UP tilts arrow up/right?
                    # Let's keep it consistent: 
                    # Angle > 0 is Right. Angle < 0 is Left.
                    # UP key -> Tilt Left? DOWN key -> Tilt Right?
                    # Let's try: UP -> Left (-), DOWN -> Right (+)
                    self.serve_angle = max(-45, self.serve_angle - aim_speed)
                if keys[pygame.K_DOWN]:
                    self.serve_angle = min(45, self.serve_angle + aim_speed)

        # Handle serving (launch ball)
        if self.is_serving and keys[pygame.K_SPACE]:
            # In local game, anyone can serve if it's their turn
            # In network game, we should filter this in main loop, but here we just execute
            if self.serving_player == 1 and (keys[pygame.K_SPACE]): # P1 serve
                 self._serve_ball()
            elif self.serving_player == 2 and (keys[pygame.K_SPACE]): # P2 serve
                 self._serve_ball()
        
        # Handle Power Shot (P key) - Direct ball to opponent king
        if keys[pygame.K_p] and not self.is_serving:
            self.direct_ball_to_king()

    def process_remote_input(self, player_id: int, input_data: Dict[str, bool]):
        """Process inputs received from network for the remote player."""
        if not input_data:
            return
            
        aim_speed = 2.0
        
        if player_id == 1:
            # Remote is Player 1 (Top)
            if input_data.get('left'):
                self.top_paddle.move(left=True, bounds=self.paddle_bounds)
            if input_data.get('right'):
                self.top_paddle.move(left=False, bounds=self.paddle_bounds)
            
            # Aiming
            if self.is_serving and self.serving_player == 1:
                if input_data.get('up'): # Aim Left
                    self.serve_angle = max(-45, self.serve_angle - aim_speed)
                if input_data.get('down'): # Aim Right
                    self.serve_angle = min(45, self.serve_angle + aim_speed)
                    
            if input_data.get('space') and self.is_serving and self.serving_player == 1:
                self._serve_ball()
            
            # Power Shot
            if input_data.get('p') and not self.is_serving:
                self.direct_ball_to_king()
                
        elif player_id == 2:
            # Remote is Player 2 (Bottom)
            if input_data.get('left'):
                self.bottom_paddle.move(left=True, bounds=self.paddle_bounds)
            if input_data.get('right'):
                self.bottom_paddle.move(left=False, bounds=self.paddle_bounds)
                
            # Aiming
            if self.is_serving and self.serving_player == 2:
                if input_data.get('up'): # Aim Left
                    self.serve_angle = max(-45, self.serve_angle - aim_speed)
                if input_data.get('down'): # Aim Right
                    self.serve_angle = min(45, self.serve_angle + aim_speed)
                    
            if input_data.get('space') and self.is_serving and self.serving_player == 2:
                self._serve_ball()
            
            # Power Shot
            if input_data.get('p') and not self.is_serving:
                self.direct_ball_to_king()

    def _serve_ball(self):
        """Launch the ball from serving state using current aim angle."""
        self.is_serving = False
        
        # Calculate velocity based on angle
        import math
        # Angle is in degrees, 0 is vertical. 
        # Positive angle -> Right, Negative -> Left
        rad = math.radians(self.serve_angle)
        
        # Total speed magnitude
        speed = max(abs(settings.BALL_SPEED_X), abs(settings.BALL_SPEED_Y))
        
        vx = speed * math.sin(rad)
        vy = speed * math.cos(rad)
        
        if self.serving_player == 1:
            self.ball.vy = abs(vy)  # Shoot down
            if self.special_bar >= self.special_bar_max:
                self.ball.is_special = True
                self.ball.current_damage = self.special_ball_damage
                self.special_just_activated = True
        else:
            self.ball.vy = -abs(vy)  # Shoot up
            if self.special_bar >= self.special_bar_max:
                self.ball.is_special = True
                self.ball.current_damage = self.special_ball_damage
                self.special_just_activated = True
            
        self.ball.vx = vx

    def update(self):
        if self.game_over or self.paused:
            return
            
        if self.is_serving:
            # Manual aiming is handled in handle_input
                
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
        # Check for special activation on paddle hit
        prev_vy = self.ball.vy
        self.ball.collide_with_paddle(self.top_paddle)
        if self.ball.vy != prev_vy: # Bounce occurred on Top Paddle (P1)
            if self.special_bar >= self.special_bar_max:
                self.ball.is_special = True
                self.ball.current_damage = self.special_ball_damage
                self.special_just_activated = True  # Mark for bar reset on first hit
            # Else: keep current state (special or normal) - do not reset

        prev_vy = self.ball.vy
        self.ball.collide_with_paddle(self.bottom_paddle)
        if self.ball.vy != prev_vy: # Bounce occurred on Bottom Paddle (P2)
            if self.special_bar >= self.special_bar_max:
                self.ball.is_special = True
                self.ball.current_damage = self.special_ball_damage
                self.special_just_activated = True  # Mark for bar reset on first hit
            # Else: keep current state (special or normal) - do not reset

        # Auto-activate special if bar is full (even without paddle touch)
        # Must be done BEFORE collision to apply special damage
        if self.special_bar >= self.special_bar_max and not self.ball.is_special:
            self.ball.is_special = True
            self.ball.current_damage = self.special_ball_damage
            self.special_just_activated = True

        # Pieces collision
        hit = self.ball.collide_with_pieces(self.board.pieces)
        if hit:
            # If special was just activated, reset the bar now on first piece hit
            if self.special_just_activated:
                self.special_bar = 0
                self.special_just_activated = False
            
            # Increment shared special bar (only if not special, or if special is active)
            # On normal hit, increment. On special hit, don't increment (would refill too fast)
            if not self.ball.is_special:
                self.special_bar = min(self.special_bar + 1, self.special_bar_max)
                
            if not hit.is_alive():
                # Add score to opponent
                points = settings.PIECE_VALUES.get(hit.type, 0)
                if hit.owner == 1:
                    self.score_p2 += points
                else:
                    self.score_p1 += points
                    
                if hit.type == "roi":
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
            'serving_player': self.serving_player,
            'serve_angle': self.serve_angle,
            'score_p1': self.score_p1,
            'score_p2': self.score_p2
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
        self.serve_angle = state.get('serve_angle', 0.0)
        self.score_p1 = state.get('score_p1', 0)
        self.score_p2 = state.get('score_p2', 0)

    def draw_navbar(self):
        """Draw the top navigation bar with scores and buttons."""
        # Background
        navbar_rect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.NAVBAR_HEIGHT)
        pygame.draw.rect(self.screen, (240, 240, 240), navbar_rect)
        pygame.draw.line(self.screen, settings.GREY, (0, settings.NAVBAR_HEIGHT), (settings.SCREEN_WIDTH, settings.NAVBAR_HEIGHT), 2)
        
        font = pygame.font.SysFont(None, 24)
        
        # Scores
        p1_text = font.render(f"P1: {self.score_p1}", True, settings.BLUE)
        self.screen.blit(p1_text, (10, settings.NAVBAR_HEIGHT // 2 - p1_text.get_height() // 2))
        
        p2_text = font.render(f"P2: {self.score_p2}", True, settings.RED)
        self.screen.blit(p2_text, (settings.SCREEN_WIDTH - p2_text.get_width() - 10, settings.NAVBAR_HEIGHT // 2 - p2_text.get_height() // 2))
        
        # Special Bar (Shared)
        bar_width = 200
        bar_height = 10
        center_x = settings.SCREEN_WIDTH // 2
        
        # Background
        bar_bg = pygame.Rect(center_x - bar_width // 2, settings.NAVBAR_HEIGHT - 15, bar_width, bar_height)
        pygame.draw.rect(self.screen, settings.GREY, bar_bg)
        pygame.draw.rect(self.screen, settings.BLACK, bar_bg, 1) # Border
        
        if self.special_bar > 0:
            fill_width = int((self.special_bar / self.special_bar_max) * bar_width)
            bar_fill = pygame.Rect(center_x - bar_width // 2, settings.NAVBAR_HEIGHT - 15, fill_width, bar_height)
            
            # Color changes when full
            color = settings.YELLOW if self.special_bar >= self.special_bar_max else (100, 100, 255)
            pygame.draw.rect(self.screen, color, bar_fill)
            
            # Glow effect if full
            if self.special_bar >= self.special_bar_max:
                pygame.draw.rect(self.screen, settings.WHITE, bar_fill, 1)
        
        # Buttons
        button_width = 100
        button_height = 30
        center_x = settings.SCREEN_WIDTH // 2
        
        # Save Button
        self.save_btn_rect = pygame.Rect(center_x - button_width - 10, settings.NAVBAR_HEIGHT // 2 - button_height // 2, button_width, button_height)
        pygame.draw.rect(self.screen, settings.GREEN, self.save_btn_rect, border_radius=5)
        save_text = font.render("Sauvegarder", True, settings.WHITE)
        self.screen.blit(save_text, save_text.get_rect(center=self.save_btn_rect.center))
        
        # Load Button
        self.load_btn_rect = pygame.Rect(center_x + 10, settings.NAVBAR_HEIGHT // 2 - button_height // 2, button_width, button_height)
        pygame.draw.rect(self.screen, settings.YELLOW, self.load_btn_rect, border_radius=5)
        load_text = font.render("Charger", True, settings.BLACK)
        self.screen.blit(load_text, load_text.get_rect(center=self.load_btn_rect.center))

    def draw_ui(self):
        # Pause overlay
        if self.paused:
            overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(settings.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.big_font.render("PAUSE", True, settings.WHITE)
            hint_text = self.font.render("Appuyez sur ESPACE pour reprendre", True, settings.WHITE)
            
            self.screen.blit(pause_text, pause_text.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 - 30)))
            self.screen.blit(hint_text, hint_text.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 + 30)))
            return
        
        # Only draw Game Over overlay here
        if self.game_over:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(settings.WHITE)
            self.screen.blit(overlay, (0, 0))
            
            msg = f"{settings.WIN_TEXT} (Gagnant: Joueur {self.winner_side})"
            text = self.big_font.render(msg, True, settings.BLACK)
            hint = self.font.render(settings.RESET_HINT, True, settings.BLACK)
            
            # Center text
            text_rect = text.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 - 30))
            hint_rect = hint.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 + 30))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(hint, hint_rect)

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.score_p1 = 0
        self.score_p2 = 0
        self.game_over = False
        self.winner_side = None
        self.is_serving = True
        self.serving_player = self.starting_player
        self.serve_angle = 0.0
        self.special_bar = 0
        self.special_just_activated = False
        
        # Reset pieces
        self.board = Board() # Re-create board to reset pieces
        # Re-apply lives configuration if needed, but Board uses settings directly?
        # Board.__init__ uses settings.CHESS_PIECES_LIVES, which we modified in apply_config.
        # So re-creating Board is enough.
        
        # Reset ball
        self.ball.reset(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.ball.vx = 0
        self.ball.vy = 0
        
        # Reset paddles
        self.top_paddle.reset()
        self.bottom_paddle.reset()

    def direct_ball_to_king(self):
        """Direct the ball towards the opponent's king based on who last touched it."""
        if self.ball.last_touched_by is None:
            print("No player has touched the ball yet.")
            return
        
        # Determine opponent
        opponent = 2 if self.ball.last_touched_by == 1 else 1
        
        # Find opponent's king
        king = None
        for piece in self.board.pieces:
            if piece.type == "roi" and piece.owner == opponent and piece.is_alive():
                king = piece
                break
        
        if king is None:
            print(f"King of player {opponent} not found or already destroyed.")
            return
        
        # Direct ball to king's center
        king_center_x = king.rect.centerx
        king_center_y = king.rect.centery
        
        self.ball.direct_to(king_center_x, king_center_y)
        #print(f"Ball directed to Player {opponent}'s King!")

    def _draw_aiming_arrow(self):
        """Draw an arrow indicating the serving direction."""
        if not self.is_serving:
            return
            
        import math
        
        # Determine start position (center of ball)
        start_pos = (self.ball.x, self.ball.y)
        
        # Calculate end position based on angle
        length = 50
        rad = math.radians(self.serve_angle)
        
        # Direction vector
        dx = length * math.sin(rad)
        dy = length * math.cos(rad)
        
        if self.serving_player == 1:
            end_pos = (start_pos[0] + dx, start_pos[1] + dy) # Down
        else:
            end_pos = (start_pos[0] + dx, start_pos[1] - dy) # Up
            
        # Draw line
        pygame.draw.line(self.screen, settings.BLACK, start_pos, end_pos, 3)
        
        # Draw arrow head
        # ... (simplified arrow head)
        pygame.draw.circle(self.screen, settings.RED, (int(end_pos[0]), int(end_pos[1])), 5)

    def draw(self):
        self.screen.fill(settings.WHITE)

        # Draw Navbar
        self.draw_navbar()

        # Board hint background (checkerboard)
        self.board.draw_board_hint(self.screen)
        # Draw paddles, ball, pieces
        self.top_paddle.draw(self.screen)
        self.bottom_paddle.draw(self.screen)
        for p in self.board.pieces:
            if p.is_alive():
                p.draw(self.screen)
        
        # Draw aiming arrow if serving
        if self.is_serving:
            self._draw_aiming_arrow()
            
        self.ball.draw(self.screen)

        self.draw_ui()
        pygame.display.flip()

    def save_game(self):
        """Save current game state to a JSON file."""
        state = self.get_game_state()
        try:
            import json
            with open("savegame.json", "w") as f:
                json.dump(state, f, indent=4)
            print("Game saved to savegame.json!")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        """Load game state from a JSON file."""
        try:
            import json
            import os
            if not os.path.exists("savegame.json"):
                print("No save file found.")
                return
                
            with open("savegame.json", "r") as f:
                state = json.load(f)
            self.set_game_state(state)
            print("Game loaded from savegame.json!")
        except Exception as e:
            print(f"Error loading game: {e}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                    
                # Reset game (R key - works anytime)
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.paused = False  # Unpause if paused
                
                # Toggle pause (SPACE key - only if not serving or game over)
                if event.key == pygame.K_SPACE:
                    if not self.is_serving and not self.game_over:
                        self.paused = not self.paused
            
            # Handle Navbar clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if hasattr(self, 'save_btn_rect') and self.save_btn_rect.collidepoint(mouse_pos):
                    self.save_game()
                elif hasattr(self, 'load_btn_rect') and self.load_btn_rect.collidepoint(mouse_pos):
                    self.load_game()

    def run(self):
        while True:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
