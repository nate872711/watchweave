"""TMDb integration stub. Enable via TMDB_ENABLED=true."""
import logging

def is_enabled(config):
    return bool(config.get('tmdb', {}).get('enabled'))
