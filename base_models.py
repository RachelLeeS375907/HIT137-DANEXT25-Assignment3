"""
base_models.py - Abstract base classes and decorators for AI models
Demonstrates: Abstraction, Encapsulation, Decorators
"""
from abc import ABC, abstractmethod
import functools
import time
from typing import Any, Callable


# Decorator 1: Timing decorator
def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to measure execution time of model inference.
    Demonstrates use of decorators for cross-cutting concerns.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[TIMING] {func.__name__} took {execution_time:.2f} seconds")
        return result
    return wrapper


# Decorator 2: Error handling decorator
def error_handler(func: Callable) -> Callable:
    """
    Decorator to handle exceptions gracefully.
    Demonstrates use of decorators for error handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"Error in {func.__name__}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return {"error": error_msg}
    return wrapper


# Abstract Base Class for all AI Models
class AIModel(ABC):
    """
    Abstract base class for AI models.
    Demonstrates: Abstraction, Encapsulation
    
    Encapsulation: Private attributes with getters/setters
    Abstraction: Abstract methods that must be implemented by subclasses
    """
    
    def __init__(self, model_name: str, description: str):
        self.__model_name = model_name  # Private attribute (encapsulation)
        self.__description = description  # Private attribute
        self._is_loaded = False  # Protected attribute
    
    # Getter methods (encapsulation)
    @property
    def model_name(self) -> str:
        return self.__model_name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def is_loaded(self) -> bool:
        return self._is_loaded
    
    # Abstract methods (must be implemented by subclasses)
    @abstractmethod
    def load_model(self) -> None:
        """Load the AI model"""
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input data through the model"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """Return model information"""
        pass


# Mixin class for logging functionality
class LoggerMixin:
    """
    Mixin class to add logging functionality.
    Demonstrates: Multiple Inheritance (used as a mixin)
    """
    
    def log_info(self, message: str) -> None:
        """Log information message"""
        print(f"[INFO] {self.__class__.__name__}: {message}")
    
    def log_error(self, message: str) -> None:
        """Log error message"""
        print(f"[ERROR] {self.__class__.__name__}: {message}")