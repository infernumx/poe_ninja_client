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
    HistoryResponse,
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
    "HistoryResponse",
    "JsonObject",
]

__version__ = "1.0.3"  # Version bump for API correction
