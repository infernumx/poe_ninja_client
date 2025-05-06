# src/poe_ninja_client/client.py

import requests
from typing import Any, Optional, cast

type JsonObject = dict[str, Any]
type JsonList = list[JsonObject]
type QueryParams = Optional[dict[str, Any]]

from .exceptions import PoeNinjaAPIError, PoeNinjaRequestError
from .enums import CurrencyType, ItemType  # GraphId removed
from .models import (
    CurrencyOverviewResponse,
    parse_currency_overview_response,
    ItemOverviewResponse,
    parse_item_overview_response,
    HistoryResponse,
    parse_history_response,
    CurrencyLine,
    ItemLine,
    CurrencyDetail,
)


class PoENinja:
    """
    A Python client for interacting with the poe.ninja API.
    The league is set during initialization and is required for all data fetching methods.
    Strictly typed for Python 3.12+.
    """

    BASE_URL: str = "https://poe.ninja/api/data"

    def __init__(
        self, league: str, user_agent: str = "Python PoENinjaClient/1.0.3"
    ):  # Version bump
        """
        Initializes the PoENinja client for a specific league.

        Args:
            league (str): The Path of Exile league to query. This is mandatory.
            user_agent (str): A User-Agent string for HTTP requests.
        """
        if not league:
            raise ValueError(
                "A league name must be provided for client initialization."
            )
        self.league: str = league
        self.session: requests.Session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def _request(self, endpoint: str, params: QueryParams = None) -> Any:
        actual_params: dict[str, Any] = params if params is not None else {}
        url: str = f"{self.BASE_URL}/{endpoint}"
        try:
            response: requests.Response = self.session.get(
                url, params=actual_params, timeout=15
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_details: str | JsonObject = ""
            if e.response is not None:
                try:
                    error_details = e.response.json()
                except requests.exceptions.JSONDecodeError:
                    error_details = e.response.text
                status_code, reason = e.response.status_code, e.response.reason
            else:
                status_code, reason = None, "Unknown reason"
            raise PoeNinjaRequestError(
                f"HTTP error: {status_code} {reason}. Details: {error_details}",
                status_code=status_code,
            ) from e
        except requests.exceptions.RequestException as e:
            raise PoeNinjaRequestError(f"Request failed: {e}") from e
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise PoeNinjaAPIError(
                f"Failed to decode JSON from {url}. Content: {response.text[:200]}..."
            ) from e

    # --- Overview Endpoints ---
    def get_currency_overview(
        self, currency_type: CurrencyType
    ) -> CurrencyOverviewResponse:
        params: dict[str, Any] = {"league": self.league, "type": currency_type.value}
        raw_data: Any = self._request("currencyoverview", params=params)
        if not isinstance(raw_data, dict):
            raise PoeNinjaAPIError(
                f"Expected JSON object for currency overview, got {type(raw_data)}"
            )
        return parse_currency_overview_response(cast(JsonObject, raw_data))

    def get_item_overview(self, item_type: ItemType) -> ItemOverviewResponse:
        params: dict[str, Any] = {"league": self.league, "type": item_type.value}
        raw_data: Any = self._request("itemoverview", params=params)
        if not isinstance(raw_data, dict):
            raise PoeNinjaAPIError(
                f"Expected JSON object for item overview, got {type(raw_data)}"
            )
        return parse_item_overview_response(cast(JsonObject, raw_data))

    # --- Find Specific Item/Currency (from overview data) ---
    def find_currency_line(
        self, name: str, currency_type: CurrencyType
    ) -> Optional[CurrencyLine]:
        """Finds a currency by name from the overview lines."""
        overview = self.get_currency_overview(currency_type=currency_type)
        name_lower = name.lower()
        for line in overview.lines:
            if line.currencyTypeName.lower() == name_lower:
                return line
        return None

    def find_item_line(
        self, name: str, item_type: ItemType
    ) -> Optional[ItemLine]:  # Renamed for clarity
        """Finds an item by name from the overview lines."""
        overview = self.get_item_overview(item_type=item_type)
        name_lower = name.lower()
        for line in overview.lines:
            if line.name.lower() == name_lower:
                return line
        return None

    # --- Helpers to get Numeric IDs for History ---
    def get_currency_id_by_name(
        self, currency_name: str, overview_type: CurrencyType = CurrencyType.CURRENCY
    ) -> Optional[int]:
        """
        Retrieves the numeric ID of a currency by its name from the 'currencyDetails' list.
        This ID is used for the 'currencyId' parameter in the currencyhistory API endpoint.
        """
        overview_data = self.get_currency_overview(currency_type=overview_type)
        name_lower = currency_name.lower()
        for detail in overview_data.currencyDetails:
            if detail.name.lower() == name_lower:
                return detail.id
        return None

    def get_item_id_by_name(self, item_name: str, item_type: ItemType) -> Optional[int]:
        """
        Retrieves the numeric ID of an item by its name from the item overview lines.
        This ID is used for the 'itemId' parameter in the itemhistory API endpoint.
        """
        overview_data = self.get_item_overview(item_type=item_type)
        name_lower = item_name.lower()
        for line in overview_data.lines:  # The numeric ID is in ItemLine.id
            if line.name.lower() == name_lower:
                return line.id
        return None

    # --- History Endpoints (Corrected based on user feedback) ---
    def get_currency_history(
        self, currency_type_for_history: CurrencyType, currency_id: int
    ) -> HistoryResponse:
        """
        Fetches historical price data for a specific currency.
        API endpoint: /currencyhistory?league={league}&type={currency_type}&currencyId={numeric_currency_id}

        Args:
            currency_type_for_history (CurrencyType): The general type of the currency
                                                      (e.g., CurrencyType.CURRENCY, CurrencyType.FRAGMENT).
            currency_id (int): The numeric ID of the currency (obtained via get_currency_id_by_name).

        Returns:
            HistoryResponse: A structured object containing historical data.
        """
        params: dict[str, Any] = {
            "league": self.league,
            "type": currency_type_for_history.value,
            "currencyId": str(currency_id),
        }
        raw_data: Any = self._request("currencyhistory", params=params)
        if not isinstance(raw_data, list):
            raise PoeNinjaAPIError(
                f"Expected JSON list for currency history data, got {type(raw_data)}"
            )
        return parse_history_response(cast(JsonList, raw_data))

    def get_item_history(
        self, item_type_for_history: ItemType, item_id: int
    ) -> HistoryResponse:
        """
        Fetches historical price data for a specific item.
        API endpoint: /itemhistory?league={league}&type={item_type}&itemId={numeric_item_id}

        Args:
            item_type_for_history (ItemType): The general type of the item
                                              (e.g., ItemType.UNIQUE_JEWEL, ItemType.UNIQUE_ARMOUR).
            item_id (int): The numeric ID of the item (obtained via get_item_id_by_name).

        Returns:
            HistoryResponse: A structured object containing historical data.
        """
        params: dict[str, Any] = {
            "league": self.league,
            "type": item_type_for_history.value,
            "itemId": str(item_id),  # API expects itemId as string
        }
        raw_data: Any = self._request("itemhistory", params=params)
        if not isinstance(raw_data, list):
            raise PoeNinjaAPIError(
                f"Expected JSON list for item history data, got {type(raw_data)}"
            )
        return parse_history_response(cast(JsonList, raw_data))

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "PoENinja":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        self.close()
