from functools import wraps
import time
import logging
def measure_time(func):
    """
    Decorator, der die Ausführungsdauer einer Funktion misst und ausgibt.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        logging.info(f"Funktion '{func.__name__}' dauerte {elapsed:.6f} Sekunden.")
        return result
    return wrapper