# logger.py
import sys
from datetime import datetime

class Logger:
    """Simple logger that writes to both console and file."""
    
    def __init__(self, filename="game_log.txt"):
        self.filename = filename
        self.file = open(filename, 'a', encoding='utf-8')
        self.file.write(f"\n{'='*50}\n")
        self.file.write(f"Game started at {datetime.now()}\n")
        self.file.write(f"{'='*50}\n")
    
    def log(self, message):
        """Log a message to both console and file."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)  # Console
        self.file.write(formatted + "\n")  # File
        self.file.flush()  # Force write to disk
    
    def close(self):
        """Close the log file."""
        self.file.write(f"\nGame ended at {datetime.now()}\n")
        self.file.close()

# Global logger instance
_logger = None

def get_logger():
    """Get or create the global logger."""
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger
