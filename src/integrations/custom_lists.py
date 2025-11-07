"""Custom Lists integration stub. Enable via CUSTOM_LISTS_ENABLED=true."""
import logging

def is_enabled(config):
    return bool(config.get('custom_lists', {}).get('enabled'))
