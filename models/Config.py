import json
from typing import Any, Dict


class Config:
    """Singleton class to manage application configuration from a JSON file."""

    _instance = None

    def __new__(cls, config_file: str = "config.json"):
        """Create a new instance of the Config class or return the existing instance.

        Args:
            config_file (str): Path to the configuration file. Defaults to "config.json".

        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config_file = config_file  # type: ignore
            cls._instance.data = cls._instance.load_config()
        return cls._instance

    def load_config(self) -> Dict[str, Any]:
        """Load configuration data from the specified JSON file.

        Returns:
            Dict[str, Any]: The configuration data as a dictionary.

        Raises:
            RuntimeError: If the configuration file is not found or contains invalid JSON.
        """
        try:
            with open(self.config_file, "r") as f:  # type: ignore
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Error loading configuration: {e}")

    @property
    def OWNER_ID(self) -> int:
        """Get the owner ID from the configuration.

        Returns:
            int: The owner ID, defaulting to 0 if not specified.
        """
        return self.data.get("owner-id", 0)

    @property
    def PREFIX(self) -> str:
        """Get the command prefix from the configuration.

        Returns:
            str: The command prefix, defaulting to "!" if not specified.
        """
        return self.data.get("prefix", "!")

    @property
    def TOKEN_LOCATION(self) -> str:
        """Get the location of the token file from the configuration.

        Returns:
            str: The token file location, defaulting to an empty string if not specified.
        """
        return self.data.get("token-location", "")

    @property
    def API_INFO_LOCATION(self) -> str:
        """Get the location of the API information file from the configuration.

        Returns:
            str: The API information file location, defaulting to an empty string if not specified.
        """
        return self.data.get("api-info-location", "")

    @property
    def RA_USERNAME(self) -> str:
        """Get the RA username from the configuration.

        Returns:
            str: The RA username, defaulting to an empty string if not specified.
        """
        return self.data.get("ra-username", "")

    def reload_config(self) -> None:
        """Reload the configuration data from the JSON file.

        This method can be used to refresh the configuration data if the file has been modified.
        """
        self.data = self.load_config()
