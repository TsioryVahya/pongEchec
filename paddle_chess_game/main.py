import pygame
import sys
import threading
from paddle_chess_game import settings
from paddle_chess_game.game import Game
from paddle_chess_game.config_menu import ConfigMenu
from paddle_chess_game.network_menu import NetworkMenu
from paddle_chess_game.network.server import GameServer
from paddle_chess_game.network.client import GameClient

def run_local_game(screen, clock):
    # Config Menu
    config_menu = ConfigMenu(screen)
    running = True
    config = None
    
    while running:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if config_menu.handle_event(event):
                config = config_menu.get_config()
                running = False
                break
        config_menu.draw()
    
    if not config:
        return

    # Game Loop
    game = Game(config)
    game.run()

def run_host_game(screen, clock, port):
    # Config Menu first
    config_menu = ConfigMenu(screen)
    running = True
    config = None
    
    while running:
        clock.tick(settings.FPS)
        for event in pygame.event.get():
            if config_menu.handle_event(event):
                config = config_menu.get_config()
                running = False
                break
        config_menu.draw()
        
    if not config:
        return

    # Start Server
    server = GameServer(port=port)
    server.start()
    
    # Wait for client
    waiting = True
    font = pygame.font.SysFont(None, 36)
    
    # Start thread to accept client so we can keep UI responsive
    client_connected = False
    
    def wait_connection():
        nonlocal client_connected
        if server.wait_for_client():
            client_connected = True
            
    threading.Thread(target=wait_connection, daemon=True).start()
    
    while waiting:
        clock.tick(settings.FPS)
        screen.fill(settings.WHITE)
        text = font.render(f"Waiting for player on port {server.port}...", True, settings.BLACK)
        screen.blit(text, (settings.SCREEN_WIDTH//2 - text.get_width()//2, settings.SCREEN_HEIGHT//2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.close()
                return
        
        if client_connected:
            waiting = False

    # Send configuration to client immediately
    server.send_config(config)

    # Game Loop (Host)
    game = Game(config)
    # Host is Player 1 (Top)
    
    running = True
    while running:
        clock.tick(settings.FPS)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Host Logic:
        # 1. Get Remote Input (Player 2)
        remote_input = server.get_client_input()
        if remote_input:
            game.process_remote_input(2, remote_input)
            
        # 2. Handle Local Input (Player 1)
        # We assume Host controls Player 1 (Top)
        # Use ARROW KEYS for Host too (more intuitive than A/D)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.top_paddle.move(left=True, bounds=game.paddle_bounds)
        if keys[pygame.K_RIGHT]:
            game.top_paddle.move(left=False, bounds=game.paddle_bounds)
        if keys[pygame.K_SPACE] and game.is_serving and game.serving_player == 1:
            game._serve_ball()
            
        # 3. Update Game
        game.update()
        
        # 4. Send State
        state = game.get_game_state()
        server.send_state(state)
        
        # 5. Draw
        game.draw()
        game.draw_ui()
        pygame.display.flip()
        
    server.close()

def run_client_game(screen, clock, ip, port):
    client = GameClient(ip, port=port)
    if not client.connect():
        print("Failed to connect")
        # Show error on screen
        font = pygame.font.SysFont(None, 32)
        screen.fill(settings.WHITE)
        
        lines = [
            "Failed to connect to server",
            f"Error: Check IP {ip} Port {port}",
            "Check Firewall settings on Host PC",
            f"Allow Python on Port {port}",
            "Ensure Server is running first"
        ]
        
        for i, line in enumerate(lines):
            color = settings.RED if i == 0 else settings.BLACK
            text = font.render(line, True, color)
            screen.blit(text, (settings.SCREEN_WIDTH//2 - text.get_width()//2, settings.SCREEN_HEIGHT//2 - 50 + i*40))
            
        pygame.display.flip()
        pygame.time.wait(4000)
        return

    # Wait for configuration
    print("Waiting for configuration...")
    config = None
    waiting_config = True
    while waiting_config:
        clock.tick(settings.FPS)
        config = client.get_config()
        if config:
            waiting_config = False
        
        # Allow quit while waiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                return

    # Client Loop
    running = True
    
    # Init Game with received config
    game = Game(config) 
    
    while running:
        clock.tick(settings.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 1. Capture Local Input (Player 2 - Bottom)
        keys = pygame.key.get_pressed()
        inputs = {
            'left': keys[pygame.K_LEFT],
            'right': keys[pygame.K_RIGHT],
            'space': keys[pygame.K_SPACE]
        }
        client.send_input(inputs)
        
        # 2. Receive State
        state = client.get_game_state()
        if state:
            game.set_game_state(state)
            
        # 3. Draw
        game.draw()
        game.draw_ui()
        pygame.display.flip()
        
    client.close()

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    
    # Network Menu
    net_menu = NetworkMenu(screen)
    mode, ip, port = net_menu.run()
    
    if mode == "local":
        run_local_game(screen, clock)
    elif mode == "host":
        run_host_game(screen, clock, port)
    elif mode == "client":
        run_client_game(screen, clock, ip, port)

if __name__ == "__main__":
    main()
