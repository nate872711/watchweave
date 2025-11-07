"""Serializd integration stub. Enable via SERIALIZD_ENABLED=true."""
import logging

def is_enabled(config):
    return bool(config.get('serializd', {}).get('enabled'))
