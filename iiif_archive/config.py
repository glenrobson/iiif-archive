import configparser
import argparse
from typing import Optional, Dict, Any
from dataclasses import dataclass

DEFAULT_INI = "conf/config.ini"

def _load(path: Optional[str]) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    files = cfg.read(path or DEFAULT_INI)
    # Not an error if missing; we’ll just use defaults in Config
    return cfg    

def _parse_bool(s: str) -> bool:
    return s.strip().lower() in {"1", "True", "true", "yes", "on"}  
  
@dataclass(frozen=True)
class Config:
    scratch_dir: str = "downloads"
    delay: int = 1
    retry_delay: int = 1
    no_delay_level0: bool = True

class Singleton:
    _instance: Config = None

def get_config():
    return Singleton._instance

def load_config(path: Optional[str] = None, overrides: Optional[Dict[str, Any]]= None) -> Config:    
    defaults = Config()
    cfg = _load(path)

    scratch_dir = cfg.get("locations", "scratch_dir", fallback=defaults.scratch_dir)
    delay = cfg.getint("Download", "delay", fallback=defaults.delay)
    retry_delay = cfg.getint("Download", "retry_delay", fallback=defaults.retry_delay)
    no_delay_level0 = _parse_bool(cfg.get("Download", "no_delay_level0", fallback=str(defaults.no_delay_level0)))

    if overrides:
        scratch_dir = overrides.get("scratch_dir", scratch_dir)
        delay = overrides.get("delay", delay)
        retry_delay = overrides.get("retry_delay", retry_delay)
        no_delay_level0 = overrides.get("no_delay_level0", no_delay_level0)

    Singleton._instance = Config(
        scratch_dir=scratch_dir,
        delay = delay,
        retry_delay = retry_delay,
        no_delay_level0 = no_delay_level0
    )    

    return Singleton._instance