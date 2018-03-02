# -*- coding: utf-8 -*-
"""Top-level package for Zwift Mobile API client."""
try:
    from .client import Client
except ImportError:
    pass
else:
    __all__ = [Client]

__author__ = """Sander Smits"""
__email__ = 'jhmsmits@gmail.com'
__version__ = '0.2.0'
