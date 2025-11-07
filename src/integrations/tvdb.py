"""TheTVDB integration stub. Enable via TVDB_ENABLED=true."""
import logging

def is_enabled(config):
    return bool(config.get('tvdb', {}).get('enabled'))
