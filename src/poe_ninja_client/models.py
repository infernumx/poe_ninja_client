# src/poe_ninja_client/models.py
from dataclasses import dataclass, field
from typing import (
    Any,
    Optional,
    List,
)  # List will be list with Python 3.9+ built-in generics

# Type alias for raw JSON objects when structure is not fully defined or varies
type JsonObject = dict[str, Any]


# --- Currency Overview Models (from previous step) ---
@dataclass(frozen=True)
class SparkLineData:
    """
    Represents the sparkline data for currency trends.
    """

    data: list[float | int] = field(default_factory=list)
    totalChange: float = 0.0


@dataclass(frozen=True)
class CurrencyTradeData:
    """
    Represents the pay or receive details for a currency.
    """

    id: int  # noqa: A003 (allow 'id' as a field name)
    league_id: int
    pay_currency_id: int
    get_currency_id: int
    sample_time_utc: str
    count: int
    value: float
    data_point_count: int
    includes_secondary: bool
    listing_count: int


@dataclass(frozen=True)
class CurrencyLine:
    """
    Represents a single currency entry in the overview.
    """

    currencyTypeName: str
    pay: Optional[CurrencyTradeData]
    receive: Optional[CurrencyTradeData]
    paySparkLine: SparkLineData
    receiveSparkLine: SparkLineData
    chaosEquivalent: float
    lowConfidencePaySparkLine: SparkLineData
    lowConfidenceReceiveSparkLine: SparkLineData
    detailsId: str


@dataclass(frozen=True)
class CurrencyOverviewResponse:
    """
    Represents the entire response from the currency overview endpoint.
    """

    lines: list[CurrencyLine]
    currencyDetails: list[JsonObject]  # Structure can vary


# --- Item Overview Models (New) ---


@dataclass(frozen=True)
class ItemSparkLine:  # Similar to SparkLineData, but some item endpoints might have different fields
    """
    Represents the sparkline data for item trends.
    """

    data: list[Optional[float | int]] = field(
        default_factory=list
    )  # Data points can sometimes be null
    totalChange: float = 0.0


@dataclass(frozen=True)
class ItemLine:
    """
    Represents a single item entry in an item overview.
    This is a generic model; specific item types might have more or fewer fields.
    Fields are marked Optional as they may not appear for all item types.
    """

    id: int  # noqa: A003
    name: str
    icon: Optional[str] = None
    mapTier: Optional[int] = None  # For maps
    levelRequired: Optional[int] = None
    baseType: Optional[str] = None
    stackSize: Optional[int] = None  # For stackable items like currency, fossils, etc.
    variant: Optional[str] = None  # E.g., for skill gems with quality types
    prophecyText: Optional[str] = None  # For prophecies
    artFilename: Optional[str] = None
    links: Optional[int] = None  # For items with links (e.g. 6-link)
    itemClass: Optional[int] = None  # Numerical class, meaning might need mapping
    sparkline: Optional[ItemSparkLine] = None
    lowConfidenceSparkline: Optional[ItemSparkLine] = None
    implicitModifiers: list[JsonObject] = field(
        default_factory=list
    )  # Structure can vary
    explicitModifiers: list[JsonObject] = field(
        default_factory=list
    )  # Structure can vary
    flavourText: Optional[str] = None
    corrupted: Optional[bool] = None
    gemLevel: Optional[int] = None  # For skill gems
    gemQuality: Optional[int] = None  # For skill gems (e.g. 20)
    itemType: Optional[str] = None  # E.g., "Abyss Jewel"
    chaosValue: Optional[float] = None
    divineValue: Optional[float] = None
    count: Optional[int] = None  # Number of items listed for this price point
    detailsId: Optional[str] = None
    # Add other common fields as identified, e.g. exaltedValue, listingCount


@dataclass(frozen=True)
class ItemOverviewResponse:
    """
    Represents the entire response from an item overview endpoint.
    """

    lines: list[ItemLine]
    # Some item endpoints might have other top-level keys, add them if needed


# --- Parser Helper Functions ---


def _parse_sparkline_data(
    data: Optional[JsonObject],
) -> SparkLineData:  # Renamed for clarity
    if data is None:
        return SparkLineData(data=[], totalChange=0.0)
    return SparkLineData(
        data=data.get("data", []), totalChange=data.get("totalChange", 0.0)
    )


def _parse_currency_trade_data(
    data: Optional[JsonObject],
) -> Optional[CurrencyTradeData]:
    if data is None:
        return None
    return CurrencyTradeData(
        id=data.get("id", 0),
        league_id=data.get("league_id", 0),
        pay_currency_id=data.get("pay_currency_id", 0),
        get_currency_id=data.get("get_currency_id", 0),
        sample_time_utc=data.get("sample_time_utc", ""),
        count=data.get("count", 0),
        value=data.get("value", 0.0),
        data_point_count=data.get("data_point_count", 0),
        includes_secondary=data.get("includes_secondary", False),
        listing_count=data.get("listing_count", 0),
    )


def _parse_currency_line(data: JsonObject) -> CurrencyLine:
    return CurrencyLine(
        currencyTypeName=data.get("currencyTypeName", "Unknown"),
        pay=_parse_currency_trade_data(data.get("pay")),
        receive=_parse_currency_trade_data(data.get("receive")),
        paySparkLine=_parse_sparkline_data(data.get("paySparkLine")),
        receiveSparkLine=_parse_sparkline_data(data.get("receiveSparkLine")),
        chaosEquivalent=data.get("chaosEquivalent", 0.0),
        lowConfidencePaySparkLine=_parse_sparkline_data(
            data.get("lowConfidencePaySparkLine")
        ),
        lowConfidenceReceiveSparkLine=_parse_sparkline_data(
            data.get("lowConfidenceReceiveSparkLine")
        ),
        detailsId=data.get("detailsId", ""),
    )


def parse_currency_overview_response(data: JsonObject) -> CurrencyOverviewResponse:
    lines_data = data.get("lines", [])
    parsed_lines = [
        _parse_currency_line(line) for line in lines_data if isinstance(line, dict)
    ]
    currency_details_data = data.get("currencyDetails", [])
    return CurrencyOverviewResponse(
        lines=parsed_lines, currencyDetails=currency_details_data
    )


# --- Item Overview Parser (New) ---


def _parse_item_sparkline(data: Optional[JsonObject]) -> Optional[ItemSparkLine]:
    if data is None:
        return None
    return ItemSparkLine(
        data=[
            val if val is not None else 0.0 for val in data.get("data", [])
        ],  # Handle potential nulls in data
        totalChange=data.get("totalChange", 0.0),
    )


def _parse_item_line(data: JsonObject) -> ItemLine:
    # This parser is generic. For specific item types, you might need
    # more sophisticated logic or different models.
    return ItemLine(
        id=data.get("id", 0),
        name=data.get("name", "Unknown Item"),
        icon=data.get("icon"),
        mapTier=data.get("mapTier"),
        levelRequired=data.get("levelRequired"),
        baseType=data.get("baseType"),
        stackSize=data.get("stackSize"),
        variant=data.get("variant"),
        prophecyText=data.get("prophecyText"),
        artFilename=data.get("artFilename"),
        links=data.get("links"),
        itemClass=data.get("itemClass"),
        sparkline=_parse_item_sparkline(data.get("sparkline")),
        lowConfidenceSparkline=_parse_item_sparkline(
            data.get("lowConfidenceSparkline")
        ),
        implicitModifiers=data.get("implicitModifiers", []),
        explicitModifiers=data.get("explicitModifiers", []),
        flavourText=data.get("flavourText"),
        corrupted=data.get("corrupted"),
        gemLevel=data.get("gemLevel"),
        gemQuality=data.get("gemQuality"),
        itemType=data.get("itemType"),
        chaosValue=data.get("chaosValue"),
        divineValue=data.get("divineValue"),
        count=data.get("count"),
        detailsId=data.get("detailsId"),
    )


def parse_item_overview_response(data: JsonObject) -> ItemOverviewResponse:
    lines_data = data.get("lines", [])
    parsed_lines = [
        _parse_item_line(line) for line in lines_data if isinstance(line, dict)
    ]
    return ItemOverviewResponse(lines=parsed_lines)
