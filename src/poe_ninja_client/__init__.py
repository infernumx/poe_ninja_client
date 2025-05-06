# src/poe_ninja_client/__init__.py

from .client import PoENinja
from .exceptions import PoeNinjaError, PoeNinjaRequestError, PoeNinjaAPIError
from .enums import (
    CurrencyType,
    ItemType,
    # GraphId removed
)
from .models import (
    SparkLineData,
    CurrencyTradeData,
    CurrencyLine,
    CurrencyOverviewResponse,
    CurrencyDetail,
    ItemSparkLine,
    ItemLine,
    ItemOverviewResponse,
    PoeNinjaHistoryDataPoint,
    CurrencyHistoryResponse,
    ItemHistoryResponse,  # Updated History models
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
    "CurrencyDetail",
    "ItemSparkLine",
    "ItemLine",
    "ItemOverviewResponse",
    "PoeNinjaHistoryDataPoint",
    "CurrencyHistoryResponse",
    "ItemHistoryResponse",
    "JsonObject",
]

__version__ = "1.0.4"  # Version bump for API correction
