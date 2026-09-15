"""
Cleanup Script for Haywire
=========================
Deletes data directories older than the retention period.
"""

import logging
import os
import shutil
from datetime import datetime, timedelta

from config import DATA_DIR, DATA_RETENTION_DAYS

logger = logging.getLogger(__name__)


def cleanup_old_data():
    """Delete data directories older than DATA_RETENTION_DAYS."""
    if not os.path.exists(DATA_DIR):
        logger.info("No data directory found. Nothing to clean up.")
        return

    cutoff = datetime.now() - timedelta(days=DATA_RETENTION_DAYS)
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    removed = 0
    kept = 0

    for entry in sorted(os.listdir(DATA_DIR)):
        entry_path = os.path.join(DATA_DIR, entry)

        if not os.path.isdir(entry_path):
            continue

        # Check if directory name is a date
        try:
            dir_date = datetime.strptime(entry, "%Y-%m-%d")
        except ValueError:
            continue

        if entry < cutoff_str:
            logger.info(f"Removing old data: {entry}")
            shutil.rmtree(entry_path)
            removed += 1
        else:
            kept += 1

    logger.info(f"Cleanup complete: removed {removed} directories, kept {kept}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    cleanup_old_data()
