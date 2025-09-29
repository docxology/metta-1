"""
DAF Profile Management

Profile-based configuration management for different use cases.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from daf.config.models import ProfileConfig


class ProfileManager:
    """Manages configuration profiles."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path("configs")
        self._profiles: Dict[str, ProfileConfig] = {}

    def load_profile(self, name: str) -> ProfileConfig:
        """Load a profile by name."""
        if name in self._profiles:
            return self._profiles[name]

        # Try to load from file
        profile_file = self.config_dir / "profiles" / f"{name}.yaml"
        if profile_file.exists():
            import yaml
            with open(profile_file, 'r') as f:
                data = yaml.safe_load(f)
                profile = ProfileConfig(**data)
                self._profiles[name] = profile
                return profile

        raise FileNotFoundError(f"Profile not found: {name}")

    def get_available_profiles(self) -> list[str]:
        """Get list of available profiles."""
        profiles = list(self._profiles.keys())

        # Check filesystem
        profile_dir = self.config_dir / "profiles"
        if profile_dir.exists():
            for file in profile_dir.glob("*.yaml"):
                profile_name = file.stem
                if profile_name not in profiles:
                    profiles.append(profile_name)

        return sorted(profiles)
