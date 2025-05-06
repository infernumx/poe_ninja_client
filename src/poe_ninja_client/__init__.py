# src/poe_ninja_client/__init__.py

from .client import PoENinja
from .exceptions import PoeNinjaError, PoeNinjaRequestError, PoeNinjaAPIError

# Expose Enums
from .enums import CurrencyType, ItemType

# Expose models for type hinting and direct use by library consumers
from .models import (
    SparkLineData,
    CurrencyTradeData,
    CurrencyLine,
    CurrencyOverviewResponse,
    ItemSparkLine,
    ItemLine,
    ItemOverviewResponse,
    JsonObject,
)

__all__ = [
    "PoENinja",
    # Exceptions
    "PoeNinjaError",
    "PoeNinjaRequestError",
    "PoeNinjaAPIError",
    # Enums
    "CurrencyType",
    "ItemType",
    # Models
    "SparkLineData",
    "CurrencyTradeData",
    "CurrencyLine",
    "CurrencyOverviewResponse",
    "ItemSparkLine",
    "ItemLine",
    "ItemOverviewResponse",
    "JsonObject",
]

__version__ = "0.5.0"  # Version bump
