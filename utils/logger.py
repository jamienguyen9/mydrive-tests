"""
Module for centralized logging configuration and utils for
the test suite. Handles log formatting, file output, and log
levels
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from configs.settings import config

def setup_logger(name: str, level: int = logging.INFO, 
                log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with specified configuration.
    
    :param name: Logger name (usually __name__)
    :param level: Logging level
    :param log_file: Optional log file name
    :returns: Configured logger instance
    """        

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = config.logs_dir / log_file
    else:
        log_path = config.logs_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)