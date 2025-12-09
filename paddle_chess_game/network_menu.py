import pygame
import sys
from paddle_chess_game import settings

class NetworkMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 48)
        self.input_font = pygame.font.SysFont(None, 32)
        
        self.options = ["Local Game", "Host Game (Server)", "Join Game (Client)"]
        self.selected_index = 0
        
        self.ip_input = "127.0.0.1"
        self.port_input = "5555"
        self.is_typing_ip = False
        self.is_typing_port = False
        
    def run(self):
        """Run the menu loop and return the selected mode, IP, and Port."""
        while True:
            self.screen.fill(settings.WHITE)
            
            # Draw title
            title = self.title_font.render("Select Game Mode", True, settings.BLACK)
            self.screen.blit(title, (settings.SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            # Draw options
            for i, option in enumerate(self.options):
                color = settings.BLUE if i == self.selected_index else settings.BLACK
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, 250 + i * 60))
                self.screen.blit(text, rect)
                
                # If "Host Game" is selected, show Port input
                if i == 1 and self.selected_index == 1:
                    port_label = self.font.render("Port:", True, settings.GREY)
                    self.screen.blit(port_label, (settings.SCREEN_WIDTH // 2 - 100, 450))
                    
                    port_color = settings.BLUE if self.is_typing_port else settings.BLACK
                    port_text = self.input_font.render(self.port_input, True, port_color)
                    port_rect = pygame.Rect(settings.SCREEN_WIDTH // 2 + 10, 445, 100, 35)
                    pygame.draw.rect(self.screen, settings.GREY, port_rect, 1)
                    self.screen.blit(port_text, (port_rect.x + 5, port_rect.y + 5))

                # If "Join Game" is selected, show IP and Port input
                if i == 2 and self.selected_index == 2:
                    # IP
                    ip_label = self.font.render("IP:", True, settings.GREY)
                    self.screen.blit(ip_label, (settings.SCREEN_WIDTH // 2 - 150, 450))
                    
                    ip_color = settings.BLUE if self.is_typing_ip else settings.BLACK
                    ip_text = self.input_font.render(self.ip_input, True, ip_color)
                    ip_rect = pygame.Rect(settings.SCREEN_WIDTH // 2 - 100, 445, 200, 35)
                    pygame.draw.rect(self.screen, settings.GREY, ip_rect, 1)
                    self.screen.blit(ip_text, (ip_rect.x + 5, ip_rect.y + 5))
                    
                    # Port
                    port_label = self.font.render("Port:", True, settings.GREY)
                    self.screen.blit(port_label, (settings.SCREEN_WIDTH // 2 + 120, 450))
                    
                    port_color = settings.BLUE if self.is_typing_port else settings.BLACK
                    port_text = self.input_font.render(self.port_input, True, port_color)
                    port_rect = pygame.Rect(settings.SCREEN_WIDTH // 2 + 180, 445, 80, 35)
                    pygame.draw.rect(self.screen, settings.GREY, port_rect, 1)
                    self.screen.blit(port_text, (port_rect.x + 5, port_rect.y + 5))

            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if self.is_typing_ip:
                        if event.key == pygame.K_RETURN:
                            self.is_typing_ip = False # Confirm IP
                        elif event.key == pygame.K_TAB:
                            self.is_typing_ip = False
                            self.is_typing_port = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.ip_input = self.ip_input[:-1]
                        else:
                            self.ip_input += event.unicode
                    elif self.is_typing_port:
                        if event.key == pygame.K_RETURN:
                            return self._get_result() # Confirm all
                        elif event.key == pygame.K_TAB:
                            self.is_typing_port = False
                            if self.selected_index == 2: self.is_typing_ip = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.port_input = self.port_input[:-1]
                        elif event.unicode.isdigit():
                            self.port_input += event.unicode
                    else:
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.selected_index == 1: # Host
                                self.is_typing_port = True
                            elif self.selected_index == 2: # Join
                                self.is_typing_ip = True
                            else:
                                return self._get_result()
                        elif event.key == pygame.K_TAB:
                            if self.selected_index == 1:
                                self.is_typing_port = not self.is_typing_port
                            elif self.selected_index == 2:
                                self.is_typing_ip = not self.is_typing_ip
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Hit testing logic (simplified)
                    # ... (omitted for brevity, keyboard is safer for now)
                    pass

    def _get_result(self):
        port = int(self.port_input) if self.port_input.isdigit() else 5555
        if self.selected_index == 0:
            return "local", None, None
        elif self.selected_index == 1:
            return "host", None, port
        else:
            return "client", self.ip_input, port
