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
            'ball_speed': max(settings.BALL_SPEED_X, settings.BALL_SPEED_Y),  # Use the higher speed as default
            'board_width': settings.BOARD_COLS,  # Number of active columns (2, 4, 6, or 8)
            'starting_player': 1,  # Player 1 starts by default
            'roi_lives': settings.CHESS_PIECES_LIVES['roi'],
            'reine_lives': settings.CHESS_PIECES_LIVES['reine'],
            'fou_lives': settings.CHESS_PIECES_LIVES['fou'],
            'tour_lives': settings.CHESS_PIECES_LIVES['tour'],
            'chevalier_lives': settings.CHESS_PIECES_LIVES['chevalier'],
            'pion_lives': settings.CHESS_PIECES_LIVES['pion'],
        }
        
        # Track which field is selected
        self.selected_field = None
        self.input_text = ""
        
        # Define input fields with positions
        self.fields = {
            'ball_speed': {'label': 'Vitesse balle', 'y': 150, 'min': 1, 'max': 20},
            'board_width': {'label': 'Largeur echiquier', 'y': 200, 'min': 2, 'max': 8, 'step': 2},  # Only even numbers
            'starting_player': {'label': 'Joueur debutant (1/2)', 'y': 250, 'min': 1, 'max': 2},
            'roi_lives': {'label': 'Vies Roi', 'y': 300, 'min': 1, 'max': 10},
            'reine_lives': {'label': 'Vies Reine', 'y': 350, 'min': 1, 'max': 10},
            'fou_lives': {'label': 'Vies Fou', 'y': 400, 'min': 1, 'max': 10},
            'tour_lives': {'label': 'Vies Tour', 'y': 450, 'min': 1, 'max': 10},
            'chevalier_lives': {'label': 'Vies Chevalier', 'y': 500, 'min': 1, 'max': 10},
            'pion_lives': {'label': 'Vies Pion', 'y': 550, 'min': 1, 'max': 10},
        }
        
        # Start button
        self.start_button_rect = pygame.Rect(
            settings.SCREEN_WIDTH // 2 - 100,
            settings.SCREEN_HEIGHT - 100,
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
                field_rect = pygame.Rect(350, field_info['y'] - 5, 80, 30)
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
        self.screen.blit(title, title.get_rect(center=(settings.SCREEN_WIDTH // 2, 60)))
        
        # Draw fields
        for field_name, field_info in self.fields.items():
            y = field_info['y']
            
            # Label
            label = self.font.render(field_info['label'] + ":", True, settings.BLACK)
            self.screen.blit(label, (100, y))
            
            # Value box
            value_text = str(self.config[field_name])
            if self.selected_field == field_name:
                value_text = self.input_text
                color = settings.BLUE
            else:
                color = settings.GREY
            
            # Draw box
            box_rect = pygame.Rect(350, y - 5, 80, 30)
            pygame.draw.rect(self.screen, color, box_rect, 2)
            
            # Draw value
            value_surface = self.font.render(value_text, True, settings.BLACK)
            self.screen.blit(value_surface, (360, y))
            
            # Draw range hint
            hint = self.small_font.render(
                f"({field_info['min']}-{field_info['max']})",
                True,
                settings.GREY
            )
            self.screen.blit(hint, (450, y + 5))
        
        # Start button
        button_color = settings.GREEN if self.start_button_rect.collidepoint(pygame.mouse.get_pos()) else settings.BLUE
        pygame.draw.rect(self.screen, button_color, self.start_button_rect)
        pygame.draw.rect(self.screen, settings.BLACK, self.start_button_rect, 3)
        
        start_text = self.font.render("COMMENCER", True, settings.WHITE)
        text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, text_rect)
        
        # Instructions
        instructions = self.small_font.render(
            "Cliquez sur une valeur pour la modifier | ESC pour quitter",
            True,
            settings.GREY
        )
        self.screen.blit(instructions, instructions.get_rect(center=(settings.SCREEN_WIDTH // 2, 600)))
        
        pygame.display.flip()
    
    def get_config(self) -> Dict[str, Any]:
        """Get the final configuration."""
        return self.config.copy()
