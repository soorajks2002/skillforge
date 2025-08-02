#!/usr/bin/env python3
"""
Logger Hierarchy Demonstration

This script demonstrates how Python's logging hierarchy works,
showing message propagation and level inheritance.
"""

import logging
import sys

def demo_basic_hierarchy():
    """Demonstrate basic logger hierarchy and propagation"""
    print("=== DEMO 1: Basic Hierarchy and Propagation ===")
    
    # Clear any existing handlers
    logging.getLogger().handlers.clear()
    
    # Create a simple formatter
    formatter = logging.Formatter('%(name)-15s | %(levelname)-8s | %(message)s')
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setFormatter(formatter)
    root_logger.addHandler(root_handler)
    root_logger.setLevel(logging.DEBUG)
    
    # Create hierarchical loggers
    app_logger = logging.getLogger('myapp')
    api_logger = logging.getLogger('myapp.api')
    db_logger = logging.getLogger('myapp.database')
    user_logger = logging.getLogger('myapp.api.user')
    
    print("Logger hierarchy:")
    print("root")
    print("└── myapp")
    print("    ├── myapp.api")
    print("    │   └── myapp.api.user")
    print("    └── myapp.database")
    print()
    
    # Log from different levels
    print("Logging from 'myapp.api.user':")
    user_logger.info("User login attempt")
    print()
    
    print("Logging from 'myapp.database':")
    db_logger.warning("Database connection slow")
    print()
    
    print("Notice: Each message appears only once because only root has a handler")
    print("All child loggers propagate their messages up to root.")
    print()

def demo_multiple_handlers():
    """Demonstrate multiple handlers at different levels"""
    print("=== DEMO 2: Multiple Handlers at Different Levels ===")
    
    # Clear existing handlers
    for logger_name in ['', 'myapp', 'myapp.api', 'myapp.database']:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
    
    # Create different formatters
    root_formatter = logging.Formatter('ROOT    | %(name)-15s | %(levelname)-8s | %(message)s')
    app_formatter = logging.Formatter('APP     | %(name)-15s | %(levelname)-8s | %(message)s')
    api_formatter = logging.Formatter('API     | %(name)-15s | %(levelname)-8s | %(message)s')
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setFormatter(root_formatter)
    root_logger.addHandler(root_handler)
    root_logger.setLevel(logging.DEBUG)
    
    # Set up app logger with its own handler
    app_logger = logging.getLogger('myapp')
    app_handler = logging.StreamHandler(sys.stdout)
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)
    app_logger.setLevel(logging.DEBUG)
    
    # Set up API logger with its own handler
    api_logger = logging.getLogger('myapp.api')
    api_handler = logging.StreamHandler(sys.stdout)
    api_handler.setFormatter(api_formatter)
    api_logger.addHandler(api_handler)
    api_logger.setLevel(logging.DEBUG)
    
    print("Now each logger has its own handler + propagation:")
    print("Logging from 'myapp.api':")
    api_logger.info("Processing API request")
    print()
    
    print("Notice: The message appears 3 times!")
    print("1. From api_logger's own handler")
    print("2. Propagated to app_logger's handler")
    print("3. Propagated to root_logger's handler")
    print()

def demo_propagation_control():
    """Demonstrate controlling propagation"""
    print("=== DEMO 3: Controlling Propagation ===")
    
    # Clear existing handlers
    for logger_name in ['', 'myapp', 'myapp.api']:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
    
    # Set up loggers with handlers
    root_logger = logging.getLogger()
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setFormatter(logging.Formatter('ROOT | %(message)s'))
    root_logger.addHandler(root_handler)
    root_logger.setLevel(logging.DEBUG)
    
    app_logger = logging.getLogger('myapp')
    app_handler = logging.StreamHandler(sys.stdout)
    app_handler.setFormatter(logging.Formatter('APP  | %(message)s'))
    app_logger.addHandler(app_handler)
    app_logger.setLevel(logging.DEBUG)
    
    api_logger = logging.getLogger('myapp.api')
    api_handler = logging.StreamHandler(sys.stdout)
    api_handler.setFormatter(logging.Formatter('API  | %(message)s'))
    api_logger.addHandler(api_handler)
    api_logger.setLevel(logging.DEBUG)
    
    print("With propagation enabled (default):")
    api_logger.info("Message with propagation")
    print()
    
    print("Disabling propagation for 'myapp.api':")
    api_logger.propagate = False
    api_logger.info("Message without propagation")
    print()
    
    print("Notice: Only the API handler processed the message")
    print()

def demo_level_inheritance():
    """Demonstrate level inheritance"""
    print("=== DEMO 4: Level Inheritance ===")
    
    # Clear existing handlers
    for logger_name in ['', 'myapp', 'myapp.api', 'myapp.database']:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setFormatter(logging.Formatter('%(name)-20s | %(levelname)-8s | %(message)s'))
    root_logger.addHandler(root_handler)
    root_logger.setLevel(logging.DEBUG)
    
    # Set up parent logger with WARNING level
    app_logger = logging.getLogger('myapp')
    app_logger.setLevel(logging.WARNING)
    
    # Child loggers - they inherit parent's level
    api_logger = logging.getLogger('myapp.api')
    db_logger = logging.getLogger('myapp.database')
    
    print("Parent 'myapp' logger level: WARNING")
    print("Child loggers inherit this level")
    print()
    
    print("Testing different message levels:")
    print("DEBUG message from 'myapp.api':")
    api_logger.debug("This won't show - below WARNING level")
    
    print("INFO message from 'myapp.api':")
    api_logger.info("This won't show - below WARNING level")
    
    print("WARNING message from 'myapp.api':")
    api_logger.warning("This will show - at WARNING level")
    
    print("ERROR message from 'myapp.database':")
    db_logger.error("This will show - above WARNING level")
    print()
    
    print("Override child logger level:")
    api_logger.setLevel(logging.DEBUG)
    print("Now 'myapp.api' level is DEBUG")
    
    print("DEBUG message from 'myapp.api' (now it will show):")
    api_logger.debug("This will show now - DEBUG level is set")
    print()

def demo_practical_usage():
    """Demonstrate practical usage patterns"""
    print("=== DEMO 5: Practical Usage Pattern ===")
    
    # Clear existing handlers
    for logger_name in ['', 'myapp', 'myapp.api', 'myapp.database', 'myapp.auth']:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
    
    # Set up main application logger
    app_logger = logging.getLogger('myapp')
    
    # Console handler for general info
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s | %(name)-15s | %(levelname)-7s | %(message)s'))
    
    # File handler for debugging (simulated with print)
    debug_handler = logging.StreamHandler(sys.stdout)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter('DEBUG | %(name)-15s | %(funcName)-10s | %(message)s'))
    
    app_logger.addHandler(console_handler)
    app_logger.addHandler(debug_handler)
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = False  # Don't propagate to root
    
    # Create component loggers
    api_logger = logging.getLogger('myapp.api')
    db_logger = logging.getLogger('myapp.database')
    auth_logger = logging.getLogger('myapp.auth')
    
    # Set different levels for different components
    api_logger.setLevel(logging.INFO)
    db_logger.setLevel(logging.DEBUG)  # More verbose for database
    auth_logger.setLevel(logging.WARNING)  # Only important auth messages
    
    print("Component loggers with different levels:")
    print("- myapp.api: INFO level")
    print("- myapp.database: DEBUG level")
    print("- myapp.auth: WARNING level")
    print()
    
    # Simulate application activity
    print("Simulating application activity:")
    
    db_logger.debug("Database connection pool initialized")
    api_logger.info("API server started on port 8000")
    auth_logger.info("This won't show - below WARNING level")
    auth_logger.warning("Failed login attempt detected")
    api_logger.error("API endpoint returned 500 error")
    
    print()
    print("Notice how different components show different levels of detail")

def main():
    """Run all demonstrations"""
    print("Python Logging Hierarchy Demonstration")
    print("=" * 50)
    print()
    
    demo_basic_hierarchy()
    input("Press Enter to continue to next demo...")
    print()
    
    demo_multiple_handlers()
    input("Press Enter to continue to next demo...")
    print()
    
    demo_propagation_control()
    input("Press Enter to continue to next demo...")
    print()
    
    demo_level_inheritance()
    input("Press Enter to continue to next demo...")
    print()
    
    demo_practical_usage()
    print()
    print("Demonstration complete!")

if __name__ == "__main__":
    main()
