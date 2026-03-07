#!/usr/bin/env python3
"""
Migration 001: Add Usage Tracking
This is a placeholder migration for Render deployment.
The application currently does not use a database.
"""

import os
import sys


def main():
    print("=" * 60)
    print("Migration 001: Add Usage Tracking")
    print("=" * 60)

    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    print(f"Data directory ensured: {data_dir}")

    # Create a marker file to indicate migration has run
    marker_file = os.path.join(data_dir, '.migration_001_complete')
    with open(marker_file, 'w') as f:
        f.write('Migration 001 completed successfully\n')
    print(f"Migration marker created: {marker_file}")

    print("Migration 001 completed successfully!")
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
