import socket
import threading
from typing import Any, Dict, Optional
from paddle_chess_game.network.utils import send_data, receive_data

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of address to avoid "Address already in use" errors
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None
        self.client_address = None
        self.running = False
        self.latest_client_input = None
        self.input_lock = threading.Lock()

    def start(self):
        """Start listening for connections."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Server started on {self.host}:{self.port}")
            self.running = True
        except Exception as e:
            print(f"Failed to start server: {e}")
            self.running = False

    def wait_for_client(self) -> bool:
        """Wait for a client to connect (blocking)."""
        if not self.running:
            return False
        
        print("Waiting for client...")
        try:
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f"Client connected from {self.client_address}")
            
            # Start input receiving thread
            input_thread = threading.Thread(target=self._receive_loop)
            input_thread.daemon = True
            input_thread.start()
            
            return True
        except Exception as e:
            print(f"Error accepting connection: {e}")
            return False

    def _receive_loop(self):
        """Background thread to receive inputs from client."""
        while self.running and self.client_socket:
            data = receive_data(self.client_socket)
            if data is None:
                print("Client disconnected")
                self.client_socket.close()
                self.client_socket = None
                break
            
            with self.input_lock:
                self.latest_client_input = data

    def get_client_input(self) -> Optional[Dict[str, bool]]:
        """Get the latest input received from client."""
        with self.input_lock:
            return self.latest_client_input

    def send_state(self, state: Dict[str, Any]):
        """Send game state to client."""
        if self.client_socket:
            send_data(self.client_socket, state)

    def send_config(self, config: Dict[str, Any]):
        """Send game configuration to client."""
        if self.client_socket:
            send_data(self.client_socket, {'type': 'config', 'data': config})

    def close(self):
        """Stop server and close connections."""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
