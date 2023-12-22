"""
UI Module
"""
from flask import Blueprint

pandemic = Blueprint("pandemic", __name__)
vaccines = Blueprint("vaccines", __name__, url_prefix="/vaccines")

from .pandemic import pandemic
from .vaccines import vaccines

__all__ = ["pandemic", "vaccines"]
