import socket
import threading
from typing import Any, Dict, Optional
from paddle_chess_game.network.utils import send_data, receive_data

class GameClient:
    def __init__(self, host: str, port: int = 5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.latest_game_state = None
        self.game_config = None
        self.state_lock = threading.Lock()

    def connect(self) -> bool:
        """Connect to the server."""
        try:
            print(f"Connecting to {self.host}:{self.port}...")
            self.socket.settimeout(5.0)  # 5 seconds timeout for connection
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)  # Remove timeout for blocking operations
            self.connected = True
            print("Connected!")
            
            # Start state receiving thread
            state_thread = threading.Thread(target=self._receive_loop)
            state_thread.daemon = True
            state_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def _receive_loop(self):
        """Background thread to receive game state from server."""
        while self.connected:
            data = receive_data(self.socket)
            if data is None:
                print("Disconnected from server")
                self.connected = False
                break
            
            # Check if it's a config message or raw state (backward compatibility or direct state)
            if isinstance(data, dict) and 'type' in data and data['type'] == 'config':
                with self.state_lock:
                    self.game_config = data['data']
            else:
                with self.state_lock:
                    self.latest_game_state = data

    def get_config(self) -> Optional[Dict[str, Any]]:
        """Get the received game configuration."""
        with self.state_lock:
            return self.game_config

    def get_game_state(self) -> Optional[Dict[str, Any]]:
        """Get the latest game state received from server."""
        with self.state_lock:
            return self.latest_game_state

    def send_input(self, inputs: Dict[str, bool]):
        """Send local input state to server."""
        if self.connected:
            send_data(self.socket, inputs)

    def close(self):
        """Close connection."""
        self.connected = False
        if self.socket:
            self.socket.close()
