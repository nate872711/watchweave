"""Musicboard integration stub. Enable via MUSICBOARD_ENABLED=true."""
import logging

def is_enabled(config):
    return bool(config.get('musicboard', {}).get('enabled'))
