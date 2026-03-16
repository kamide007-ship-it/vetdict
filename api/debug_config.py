import os


def is_debug_mode_enabled():
    return os.getenv('FLASK_DEBUG', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
