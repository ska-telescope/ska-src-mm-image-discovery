import logging
import os
import re

import yaml

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class ConfigClient:
    logger = logging.getLogger("uvicorn")
    # Regex patterns for placeholders
    env_var_pattern = re.compile(r'\$\{(\w+)}')  # Matches ${ENV_KEY}
    env_var_with_default_pattern = re.compile(r'\$\{(\w+):([^}]+)}')  # Matches ${ENV_KEY:DEFAULT_VAL}

    def __init__(self, config_file_name="resources/app.yaml"):
        config_path = self.get_project_src(config_file_name)
        self.config = self.load_and_process_yaml(config_path)

    def get_project_src(self, config_file_name: str):
        source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        config_path = f"{source_path}/{config_file_name}"
        self.logger.debug(f"Loading configuration from {config_path}")
        return config_path

    def load_and_process_yaml(self, file_path: str):
        with open(file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)
        yaml_content = self.process_object(yaml_content)
        return yaml_content

    def process_object(self, obj):
        if isinstance(obj, list):
            return [self.process_object(item) for item in obj]
        elif isinstance(obj, dict):
            for key, val in obj.items():
                obj[key] = self.process_object(val)
            return obj
        return self.resolve_placeholders(obj)

    def resolve_placeholders(self, value):
        if isinstance(value, str):
            # Handle ${ENV_KEY:DEFAULT_VAL}
            match_with_default = self.env_var_with_default_pattern.search(value)
            if match_with_default:
                env_key, default_val = match_with_default.groups()
                return os.getenv(env_key, default_val)
            # Handle ${ENV_KEY}
            match = self.env_var_pattern.search(value)
            if match:
                env_key = match.group(1)
                if env_key in os.environ:
                    return os.getenv(env_key)
                else:
                    raise ValueError(f"Environment variable '{env_key}' is not set")
        return value

    def get(self, key: str, default=None):
        keys = key.split('.')
        cfg = self.config
        for k in keys:
            if k in cfg:
                cfg = cfg[k]
            else:
                if default is not None:
                    return default
                else:
                    raise KeyError(f"Key '{key}' not found in configuration")
        return cfg

    def get_string(self, key: str, default=str | None) -> str:
        cfg = self.get(key, default)
        if not isinstance(cfg, str):
            raise ValueError(f"value for key '{key}' is not a string")
        return cfg

    def get_list(self, key: str, default=list | None) -> list:
        cfg = self.get(key, default)
        if not isinstance(cfg, list):
            raise ValueError(f"value for key '{key}' is not a list")
        return cfg

    def get_dict(self, key: str, default=dict | None) -> dict:
        cfg = self.get(key, default)
        if not isinstance(cfg, dict):
            raise ValueError(f"value for key '{key}' is not a dict")
        return cfg

    def load(self, key: str, cls, default=None):
        try:
            cfg = self.get_dict(key)
            if not isinstance(cfg, dict):
                raise ValueError(f"value for key '{key}' is not a dict")
            return cls(**cfg)
        except Exception as e:
            if default is None:
                raise e
            return default
