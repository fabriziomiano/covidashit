"""Logging helper for ETL modules."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured module logger without duplicate stream handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
        logger.addHandler(handler)

    return logger
