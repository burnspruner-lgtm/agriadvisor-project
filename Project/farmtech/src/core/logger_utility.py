import logging

class LoggerUtility:
    """Extracted utility for centralized and standardized system logging."""
    LOG_FORMAT = "[%(asctime)s] | %(levelname)s | [%(threadName)s] | %(module)s.%(funcName)s: %(message)s"
    
    @staticmethod
    def setup_logging(level=logging.INFO):
        """Initializes logging configuration for all modules."""
        logging.basicConfig(level=level, 
                            format=LoggerUtility.LOG_FORMAT, 
                            datefmt='%Y-%m-%d %H:%M:%S')

# Initialize logging immediately upon import
LoggerUtility.setup_logging()