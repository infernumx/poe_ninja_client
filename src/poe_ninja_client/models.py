# src/poe_ninja_client/models.py
from dataclasses import dataclass, field
from typing import Any, Optional, List, cast

# Type alias for raw JSON objects when structure is not fully defined or varies
type JsonObject = dict[str, Any]
type JsonList = list[JsonObject]


# --- Currency Overview Models ---
@dataclass(frozen=True)
class SparkLineData:
    data: list[float | int] = field(default_factory=list)
    totalChange: float = 0.0


@dataclass(frozen=True)
class CurrencyTradeData:
    id: int  # noqa: A003
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
    currencyTypeName: str
    pay: Optional[CurrencyTradeData]
    receive: Optional[CurrencyTradeData]
    paySparkLine: SparkLineData
    receiveSparkLine: SparkLineData
    chaosEquivalent: float
    lowConfidencePaySparkLine: SparkLineData
    lowConfidenceReceiveSparkLine: SparkLineData
    detailsId: str  # This is the string ID like "chaos-orb", "divine-orb"


@dataclass(frozen=True)
class CurrencyDetail:
    """Represents a currency item listed in the currencyDetails part of an overview."""

    id: int  # Numeric ID, used for currencyhistory typeId
    name: str
    icon: Optional[str] = None
    tradeId: Optional[str] = None  # String ID, e.g., "divine", "chaos"


@dataclass(frozen=True)
class CurrencyOverviewResponse:
    lines: list[CurrencyLine]
    currencyDetails: list[CurrencyDetail]


# --- Item Overview Models ---
@dataclass(frozen=True)
class ItemSparkLine:
    data: list[Optional[float | int]] = field(default_factory=list)
    totalChange: float = 0.0


@dataclass(frozen=True)
class ItemLine:
    id: int  # noqa: A003
    name: str
    icon: Optional[str] = None
    mapTier: Optional[int] = None
    levelRequired: Optional[int] = None
    baseType: Optional[str] = None
    stackSize: Optional[int] = None
    variant: Optional[str] = None
    prophecyText: Optional[str] = None
    artFilename: Optional[str] = None
    links: Optional[int] = None
    itemClass: Optional[int] = None
    sparkline: Optional[ItemSparkLine] = None
    lowConfidenceSparkline: Optional[ItemSparkLine] = None
    implicitModifiers: list[JsonObject] = field(default_factory=list)
    explicitModifiers: list[JsonObject] = field(default_factory=list)
    flavourText: Optional[str] = None
    corrupted: Optional[bool] = None
    gemLevel: Optional[int] = None
    gemQuality: Optional[int] = None
    itemType: Optional[str] = None
    chaosValue: Optional[float] = None
    divineValue: Optional[float] = None
    count: Optional[int] = None
    detailsId: Optional[str] = None  # This is the string ID used for itemhistory typeId


@dataclass(frozen=True)
class ItemOverviewResponse:
    lines: list[ItemLine]


# --- History Endpoint Models (Refined for Currency History) ---
@dataclass(frozen=True)
class PoeNinjaHistoryDataPoint:
    daysAgo: int
    value: float


@dataclass(frozen=True)
class CurrencyHistoryResponse:  # Specific to currencyhistory endpoint structure
    """
    Represents a structured response from the currencyhistory endpoint.
    Contains 'pay' and 'receive' graph data.
    """

    receive_currency_graph_data: list[PoeNinjaHistoryDataPoint] = field(
        default_factory=list
    )
    pay_currency_graph_data: list[PoeNinjaHistoryDataPoint] = field(
        default_factory=list
    )
    # Other potential top-level fields from the response can be added here.


@dataclass(frozen=True)
class ItemHistoryResponse:  # For itemhistory endpoint (assuming simple list for now)
    """
    Represents a structured response from the itemhistory endpoint.
    Assuming this endpoint returns a simple list of data points directly.
    If it also returns a complex object, this model will need adjustment.
    """

    data_points: list[PoeNinjaHistoryDataPoint] = field(default_factory=list)


# --- Parser Helper Functions ---
def _parse_sparkline_data(data: Optional[JsonObject]) -> SparkLineData:
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


def _parse_currency_detail(data: JsonObject) -> CurrencyDetail:
    return CurrencyDetail(
        id=data.get("id", 0),
        icon=data.get("icon"),
        name=data.get("name", "Unknown Currency Detail"),
        tradeId=data.get("tradeId"),
    )


def parse_currency_overview_response(data: JsonObject) -> CurrencyOverviewResponse:
    lines_data = data.get("lines", [])
    parsed_lines = [
        _parse_currency_line(line) for line in lines_data if isinstance(line, dict)
    ]

    currency_details_raw = data.get("currencyDetails", [])
    parsed_currency_details = [
        _parse_currency_detail(detail)
        for detail in currency_details_raw
        if isinstance(detail, dict)
    ]

    return CurrencyOverviewResponse(
        lines=parsed_lines, currencyDetails=parsed_currency_details
    )


def _parse_item_sparkline(data: Optional[JsonObject]) -> Optional[ItemSparkLine]:
    if data is None:
        return None
    return ItemSparkLine(
        data=[val if val is not None else 0.0 for val in data.get("data", [])],
        totalChange=data.get("totalChange", 0.0),
    )


def _parse_item_line(data: JsonObject) -> ItemLine:
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


def _parse_history_data_point_list(
    raw_data_list: Optional[JsonList],
) -> list[PoeNinjaHistoryDataPoint]:
    """Helper to parse a list of raw history data points."""
    if raw_data_list is None:
        return []

    parsed_data_points: list[PoeNinjaHistoryDataPoint] = []
    for point_data in raw_data_list:
        if isinstance(point_data, dict):
            days_ago = point_data.get("daysAgo")
            value = point_data.get("value")
            if isinstance(days_ago, int) and isinstance(value, (float, int)):
                parsed_data_points.append(
                    PoeNinjaHistoryDataPoint(daysAgo=days_ago, value=float(value))
                )
    return parsed_data_points


def parse_currency_history_response(
    raw_response_object: JsonObject,
) -> CurrencyHistoryResponse:
    """
    Parses the JSON object response from the currencyhistory endpoint.
    Expects an object with 'receiveCurrencyGraphData' and 'payCurrencyGraphData' keys,
    each containing a list of history data points.
    """
    receive_data = raw_response_object.get("receiveCurrencyGraphData")
    pay_data = raw_response_object.get("payCurrencyGraphData")

    parsed_receive_data = _parse_history_data_point_list(
        cast(Optional[JsonList], receive_data)
    )
    parsed_pay_data = _parse_history_data_point_list(cast(Optional[JsonList], pay_data))

    return CurrencyHistoryResponse(
        receive_currency_graph_data=parsed_receive_data,
        pay_currency_graph_data=parsed_pay_data,
    )


def parse_item_history_response(raw_history_data_list: JsonList) -> ItemHistoryResponse:
    """
    Parses the list of raw history data points from the itemhistory endpoint.
    Assuming itemhistory returns a simple list of data points.
    """
    parsed_data_points = _parse_history_data_point_list(raw_history_data_list)
    return ItemHistoryResponse(data_points=parsed_data_points)
