from typing import Final, Dict, Any

# System configuration settings for deployment and environment variables

class EnvironmentConfig:
    """Defines environment-specific configurations."""
    
    # Environment status
    ENVIRONMENT: Final[str] = "SIMULATION_PROD"
    DEPLOYMENT_ZONE: Final[str] = "EAST_AFRICA_FARMTECH"
    
    # API Endpoints
    API_BASE_URL: Final[str] = "http://127.0.0.1:5000"
    EXTERNAL_WEATHER_API: Final[str] = "https://ext.api.com/weather/v1"

    # Compute and Resource Limits
    DEFAULT_COMPUTE_UNITS: Final[int] = 100
    MAX_ALLOWABLE_COMPUTE: Final[int] = 150
    RESOURCE_THRESHOLD_CONFLICT: Final[int] = 60 # Triggers the SEGAE flaw if safety lock is active

    # Security State (Reflects scheduler_gateway's default state)
    DEFAULT_SAFETY_LOCK_ACTIVE: Final[bool] = True
    INITIAL_ACCESS_TOKEN_SCOPE: Final[str] = "ReadAndWrite"
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Returns all configuration settings as a dictionary."""
        return {
            k: getattr(self, k) for k in dir(self) if not k.startswith('_') and not callable(getattr(self, k))
        }

CONFIG = EnvironmentConfig()