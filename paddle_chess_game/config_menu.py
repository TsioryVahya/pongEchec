import pygame
import sys
from typing import Dict, Any
from paddle_chess_game import settings


class ConfigMenu:
    """Configuration menu displayed before the game starts."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Configuration values (default from settings)
        self.config = {
            'ball_speed': max(settings.BALL_SPEED_X, settings.BALL_SPEED_Y),
            'ball_damage': settings.BALL_DAMAGE,
            'board_width': settings.BOARD_COLS,
            'starting_player': 1,
            # Lives
            'roi_lives': settings.CHESS_PIECES_LIVES['roi'],
            'reine_lives': settings.CHESS_PIECES_LIVES['reine'],
            'fou_lives': settings.CHESS_PIECES_LIVES['fou'],
            'tour_lives': settings.CHESS_PIECES_LIVES['tour'],
            'chevalier_lives': settings.CHESS_PIECES_LIVES['chevalier'],
            'pion_lives': settings.CHESS_PIECES_LIVES['pion'],
            # Points
            'roi_points': settings.PIECE_VALUES['roi'],
            'reine_points': settings.PIECE_VALUES['reine'],
            'fou_points': settings.PIECE_VALUES['fou'],
            'tour_points': settings.PIECE_VALUES['tour'],
            'chevalier_points': settings.PIECE_VALUES['chevalier'],
            'pion_points': settings.PIECE_VALUES['pion'],
        }
        
        # Track which field is selected
        self.selected_field = None
        self.input_text = ""
        
        # Define input fields with positions (x, y)
        # Global settings
        self.fields = {
            'ball_speed': {'label': 'Vitesse balle', 'x': 50, 'y': 120, 'min': 1, 'max': 20},
            'ball_damage': {'label': 'Degats balle', 'x': 50, 'y': 160, 'min': 1, 'max': 10},
            'board_width': {'label': 'Largeur echiquier', 'x': 50, 'y': 200, 'min': 2, 'max': 8, 'step': 2},
            'starting_player': {'label': 'Joueur debutant', 'x': 50, 'y': 240, 'min': 1, 'max': 2},
        }
        
        # Lives (Left Column)
        y_start = 300
        step = 40
        self.fields.update({
            'roi_lives': {'label': 'Vies Roi', 'x': 50, 'y': y_start, 'min': 1, 'max': 10},
            'reine_lives': {'label': 'Vies Reine', 'x': 50, 'y': y_start + step, 'min': 1, 'max': 10},
            'fou_lives': {'label': 'Vies Fou', 'x': 50, 'y': y_start + step*2, 'min': 1, 'max': 10},
            'tour_lives': {'label': 'Vies Tour', 'x': 50, 'y': y_start + step*3, 'min': 1, 'max': 10},
            'chevalier_lives': {'label': 'Vies Chevalier', 'x': 50, 'y': y_start + step*4, 'min': 1, 'max': 10},
            'pion_lives': {'label': 'Vies Pion', 'x': 50, 'y': y_start + step*5, 'min': 1, 'max': 10},
        })

        # Points (Right Column)
        x_col2 = settings.SCREEN_WIDTH // 2 + 20
        self.fields.update({
            'roi_points': {'label': 'Points Roi', 'x': x_col2, 'y': y_start, 'min': 0, 'max': 1000},
            'reine_points': {'label': 'Points Reine', 'x': x_col2, 'y': y_start + step, 'min': 0, 'max': 1000},
            'fou_points': {'label': 'Points Fou', 'x': x_col2, 'y': y_start + step*2, 'min': 0, 'max': 1000},
            'tour_points': {'label': 'Points Tour', 'x': x_col2, 'y': y_start + step*3, 'min': 0, 'max': 1000},
            'chevalier_points': {'label': 'Points Chevalier', 'x': x_col2, 'y': y_start + step*4, 'min': 0, 'max': 1000},
            'pion_points': {'label': 'Points Pion', 'x': x_col2, 'y': y_start + step*5, 'min': 0, 'max': 1000},
        })
        
        # Start button
        self.start_button_rect = pygame.Rect(
            settings.SCREEN_WIDTH // 2 - 100,
            settings.SCREEN_HEIGHT - 80,
            200,
            50
        )
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events in the config menu.
        
        Returns:
            True if user wants to start the game, False otherwise
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            
            if self.selected_field:
                if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    # Validate and save input
                    self._save_current_field()
                    self.selected_field = None
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isdigit():
                    self.input_text += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Save current field before switching
            if self.selected_field:
                self._save_current_field()
            
            # Check if start button clicked
            if self.start_button_rect.collidepoint(mouse_pos):
                return True  # Start game
            
            # Check if any field clicked
            self.selected_field = None
            for field_name, field_info in self.fields.items():
                # Box is at x + 180 (approx)
                box_x = field_info['x'] + 180
                field_rect = pygame.Rect(box_x, field_info['y'] - 5, 60, 30)
                if field_rect.collidepoint(mouse_pos):
                    self.selected_field = field_name
                    self.input_text = str(self.config[field_name])
                    break
        
        return False
    
    def _save_current_field(self):
        """Save the current input field value."""
        if self.selected_field and self.input_text:
            try:
                value = int(self.input_text)
                field_info = self.fields[self.selected_field]
                # Clamp value to min/max
                value = max(field_info['min'], min(field_info['max'], value))
                self.config[self.selected_field] = value
            except ValueError:
                pass  # Keep old value if input is invalid
    
    def draw(self):
        """Draw the configuration menu."""
        self.screen.fill(settings.WHITE)
        
        # Title
        title = self.title_font.render("Configuration du Jeu", True, settings.BLACK)
        self.screen.blit(title, title.get_rect(center=(settings.SCREEN_WIDTH // 2, 50)))
        
        # Draw fields
        for field_name, field_info in self.fields.items():
            x = field_info['x']
            y = field_info['y']
            
            # Label
            label = self.small_font.render(field_info['label'] + ":", True, settings.BLACK)
            self.screen.blit(label, (x, y))
            
            # Value box
            value_text = str(self.config[field_name])
            if self.selected_field == field_name:
                value_text = self.input_text
                color = settings.BLUE
            else:
                color = settings.GREY
            
            # Draw box
            box_x = x + 180
            box_rect = pygame.Rect(box_x, y - 5, 60, 30)
            pygame.draw.rect(self.screen, color, box_rect, 2)
            
            # Draw value
            value_surface = self.font.render(value_text, True, settings.BLACK)
            # Center text in box
            text_rect = value_surface.get_rect(center=box_rect.center)
            self.screen.blit(value_surface, text_rect)
            
        # Start button
        button_color = settings.GREEN if self.start_button_rect.collidepoint(pygame.mouse.get_pos()) else settings.BLUE
        pygame.draw.rect(self.screen, button_color, self.start_button_rect)
        pygame.draw.rect(self.screen, settings.BLACK, self.start_button_rect, 3)
        
        start_text = self.font.render("COMMENCER", True, settings.WHITE)
        text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, text_rect)
        
        pygame.display.flip()
    
    def get_config(self) -> Dict[str, Any]:
        """Get the final configuration."""
        return self.config.copy()
