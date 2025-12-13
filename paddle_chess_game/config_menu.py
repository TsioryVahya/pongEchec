import pygame
import sys
from typing import Dict, Any
from paddle_chess_game import settings
from paddle_chess_game.services.config_service import ConfigurationService


class ConfigMenu:
    """Configuration menu displayed before the game starts."""
    
    # Colors
    BG_COLOR = (30, 30, 40)
    TEXT_COLOR = (240, 240, 240)
    INPUT_BG = (50, 50, 60)
    INPUT_BORDER = (100, 100, 120)
    INPUT_ACTIVE = (70, 130, 180)
    BUTTON_BG = (60, 160, 80)
    BUTTON_HOVER = (80, 180, 100)
    SERVER_BTN_BG = (70, 130, 180)
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 18)
        
        # Backend Service
        self.config_service = ConfigurationService("http://localhost:8080/pongechec/api")
        self.server_configs = []
        self.status_message = ""
        self.status_timer = 0
        
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
        
        self.selected_field = None
        self.input_text = ""
        
        # Define fields metadata
        self.fields_meta = {
            'ball_speed': {'label': 'Vitesse balle', 'min': 1, 'max': 20},
            'ball_damage': {'label': 'Dégâts balle', 'min': 1, 'max': 10},
            'board_width': {'label': 'Largeur échiquier', 'min': 2, 'max': 8, 'step': 2},
            'starting_player': {'label': 'Joueur débutant', 'min': 1, 'max': 2},
            
            'roi_lives': {'label': 'Vies Roi', 'min': 1, 'max': 10},
            'reine_lives': {'label': 'Vies Reine', 'min': 1, 'max': 10},
            'fou_lives': {'label': 'Vies Fou', 'min': 1, 'max': 10},
            'tour_lives': {'label': 'Vies Tour', 'min': 1, 'max': 10},
            'chevalier_lives': {'label': 'Vies Chevalier', 'min': 1, 'max': 10},
            'pion_lives': {'label': 'Vies Pion', 'min': 1, 'max': 10},
            
            'roi_points': {'label': 'Points Roi', 'min': 0, 'max': 1000},
            'reine_points': {'label': 'Points Reine', 'min': 0, 'max': 1000},
            'fou_points': {'label': 'Points Fou', 'min': 0, 'max': 1000},
            'tour_points': {'label': 'Points Tour', 'min': 0, 'max': 1000},
            'chevalier_points': {'label': 'Points Chevalier', 'min': 0, 'max': 1000},
            'pion_points': {'label': 'Points Pion', 'min': 0, 'max': 1000},
        }
        
        self._recalculate_layout()
        
    def _recalculate_layout(self):
        """Recalculate positions based on screen size."""
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Center column x
        col1_x = self.width * 0.15
        col2_x = self.width * 0.45
        col3_x = self.width * 0.75
        
        start_y = self.height * 0.2
        step_y = 50
        
        self.ui_elements = {}
        
        # General Settings (Col 1)
        general_keys = ['ball_speed', 'ball_damage', 'board_width', 'starting_player']
        for i, key in enumerate(general_keys):
            self.ui_elements[key] = {
                'label_pos': (col1_x, start_y + i * step_y),
                'input_rect': pygame.Rect(col1_x + 150, start_y + i * step_y - 5, 80, 35)
            }
            
        # Lives (Col 2)
        lives_keys = ['roi_lives', 'reine_lives', 'fou_lives', 'tour_lives', 'chevalier_lives', 'pion_lives']
        for i, key in enumerate(lives_keys):
            self.ui_elements[key] = {
                'label_pos': (col2_x, start_y + i * step_y),
                'input_rect': pygame.Rect(col2_x + 150, start_y + i * step_y - 5, 80, 35)
            }
            
        # Points (Col 3)
        points_keys = ['roi_points', 'reine_points', 'fou_points', 'tour_points', 'chevalier_points', 'pion_points']
        for i, key in enumerate(points_keys):
            self.ui_elements[key] = {
                'label_pos': (col3_x, start_y + i * step_y),
                'input_rect': pygame.Rect(col3_x + 150, start_y + i * step_y - 5, 80, 35)
            }
            
        # Buttons
        btn_width = 220
        btn_height = 50
        margin = 20
        
        # Start Button (Center Bottom)
        self.start_btn_rect = pygame.Rect(
            (self.width - btn_width) // 2,
            self.height - 80,
            btn_width,
            btn_height
        )
        
        # Server Buttons (Bottom Left/Right)
        self.load_btn_rect = pygame.Rect(margin, self.height - 70, 180, 40)
        self.save_btn_rect = pygame.Rect(self.width - 180 - margin, self.height - 70, 180, 40)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
            
        if event.type == pygame.VIDEORESIZE:
            self._recalculate_layout()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            
            if self.selected_field:
                if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
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
            
            # Check Buttons
            if self.start_btn_rect.collidepoint(mouse_pos):
                return True
            if self.load_btn_rect.collidepoint(mouse_pos):
                self._load_from_server()
                return False
            if self.save_btn_rect.collidepoint(mouse_pos):
                self._save_to_server()
                return False
                
            # Check Input Fields
            self.selected_field = None
            for key, element in self.ui_elements.items():
                if element['input_rect'].collidepoint(mouse_pos):
                    self.selected_field = key
                    self.input_text = str(self.config[key])
                    break
                    
        return False

    def _load_from_server(self):
        if self.config_service.test_connection():
            self.server_configs = self.config_service.get_all_configurations()
            if self.server_configs:
                # Mode Singleton: On charge directement la première configuration
                config = self.server_configs[0]
                self._apply_config(config)
                self.status_message = f"Configuration chargée!"
            else:
                self.status_message = "Aucune configuration trouvée."
        else:
            self.status_message = "Erreur: Backend inaccessible!"
        self.status_timer = pygame.time.get_ticks() + 3000

    def _save_to_server(self):
        if self.config_service.test_connection():
            # Mode Singleton: On garde un nom fixe
            name = "Configuration Standard"
            result = self.config_service.save_configuration(self.config, name)
            if result:
                self.status_message = "Configuration sauvegardée!"
            else:
                self.status_message = "Erreur lors de la sauvegarde."
        else:
            self.status_message = "Erreur: Backend inaccessible!"
        self.status_timer = pygame.time.get_ticks() + 3000

    def _apply_config(self, config):
        for key in self.config:
            if key in config:
                self.config[key] = config[key]

    def _save_current_field(self):
        if self.selected_field and self.input_text:
            try:
                value = int(self.input_text)
                meta = self.fields_meta[self.selected_field]
                value = max(meta['min'], min(meta['max'], value))
                self.config[self.selected_field] = value
            except ValueError:
                pass

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title = self.title_font.render("CONFIGURATION DU JEU", True, self.TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 50)))
        
        # Draw Fields
        for key, element in self.ui_elements.items():
            label_pos = element['label_pos']
            rect = element['input_rect']
            
            # Label
            label = self.font.render(self.fields_meta[key]['label'], True, self.TEXT_COLOR)
            self.screen.blit(label, label_pos)
            
            # Input Box
            color = self.INPUT_ACTIVE if self.selected_field == key else self.INPUT_BORDER
            pygame.draw.rect(self.screen, self.INPUT_BG, rect, border_radius=5)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=5)
            
            # Value
            val_text = self.input_text if self.selected_field == key else str(self.config[key])
            text_surf = self.font.render(val_text, True, self.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            
        # Draw Buttons
        # Start
        mouse_pos = pygame.mouse.get_pos()
        start_color = self.BUTTON_HOVER if self.start_btn_rect.collidepoint(mouse_pos) else self.BUTTON_BG
        pygame.draw.rect(self.screen, start_color, self.start_btn_rect, border_radius=10)
        start_txt = self.title_font.render("JOUER", True, settings.WHITE)
        start_txt = pygame.transform.scale(start_txt, (int(start_txt.get_width()*0.7), int(start_txt.get_height()*0.7)))
        self.screen.blit(start_txt, start_txt.get_rect(center=self.start_btn_rect.center))
        
        # Server Buttons
        load_color = self.BUTTON_HOVER if self.load_btn_rect.collidepoint(mouse_pos) else self.SERVER_BTN_BG
        pygame.draw.rect(self.screen, load_color, self.load_btn_rect, border_radius=8)
        load_txt = self.small_font.render("Charger (Serveur)", True, settings.WHITE)
        self.screen.blit(load_txt, load_txt.get_rect(center=self.load_btn_rect.center))
        
        save_color = self.BUTTON_HOVER if self.save_btn_rect.collidepoint(mouse_pos) else self.SERVER_BTN_BG
        pygame.draw.rect(self.screen, save_color, self.save_btn_rect, border_radius=8)
        save_txt = self.small_font.render("Sauver (Serveur)", True, settings.WHITE)
        self.screen.blit(save_txt, save_txt.get_rect(center=self.save_btn_rect.center))
        
        # Status Message
        if self.status_message and pygame.time.get_ticks() < self.status_timer:
            status = self.font.render(self.status_message, True, (255, 100, 100))
            self.screen.blit(status, status.get_rect(center=(self.width//2, self.height - 120)))
            
        pygame.display.flip()

    def get_config(self) -> Dict[str, Any]:
        return self.config.copy()
