import socket
import struct
import pickle
from typing import Any, Optional

def send_data(sock: socket.socket, data: Any):
    """Send data with length prefix."""
    try:
        serialized = pickle.dumps(data)
        # Prefix with length (4 bytes network byte order)
        message = struct.pack('!I', len(serialized)) + serialized
        sock.sendall(message)
    except Exception as e:
        print(f"Error sending data: {e}")

def receive_data(sock: socket.socket) -> Optional[Any]:
    """Receive data with length prefix."""
    try:
        # Read length prefix
        length_data = recv_all(sock, 4)
        if not length_data:
            return None
        
        length = struct.unpack('!I', length_data)[0]
        
        # Read data
        data = recv_all(sock, length)
        if not data:
            return None
            
        return pickle.loads(data)
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def recv_all(sock: socket.socket, n: int) -> Optional[bytes]:
    """Helper to receive exactly n bytes."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
