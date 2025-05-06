# src/poe_ninja_client/client.py

import requests
from typing import Any, Optional

# Type aliases for better readability using Python 3.12 `type` keyword
type JsonObject = dict[str, Any]
type QueryParams = Optional[dict[str, Any]]

from .exceptions import PoeNinjaAPIError, PoeNinjaRequestError
from .enums import CurrencyType, ItemType  # New import for Enums
from .models import (
    CurrencyOverviewResponse,
    parse_currency_overview_response,
    ItemOverviewResponse,
    parse_item_overview_response,
    CurrencyLine,
    ItemLine,
)


class PoENinja:
    """
    A Python client for interacting with the poe.ninja API.
    The league is set during initialization.
    Strictly typed for Python 3.12+.
    """

    BASE_URL: str = "https://poe.ninja/api/data"

    def __init__(
        self, league: str, user_agent: str = "Python PoENinjaClient/0.5.0"
    ):  # Version bump
        """
        Initializes the PoENinja client for a specific league.

        Args:
            league (str): The Path of Exile league to query (e.g., "Necropolis").
            user_agent (str): A User-Agent string for HTTP requests.
        """
        if not league:
            raise ValueError("League cannot be empty.")
        self.league: str = league
        self.session: requests.Session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def _request(self, endpoint: str, params: QueryParams = None) -> JsonObject:
        """
        Makes a GET request to the specified poe.ninja API endpoint.
        Internal method, returns raw JSON object.

        Args:
            endpoint (str): The API endpoint to call (e.g., "currencyoverview").
            params (QueryParams): A dictionary of query parameters.

        Returns:
            JsonObject: The JSON response from the API.

        Raises:
            PoeNinjaRequestError: If there's a network issue or non-200 status code.
            PoeNinjaAPIError: If the API returns an error message or unexpected format.
        """
        actual_params: dict[str, Any] = params if params is not None else {}
        url: str = f"{self.BASE_URL}/{endpoint}"

        try:
            response: requests.Response = self.session.get(
                url, params=actual_params, timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_details: str | JsonObject = ""
            if e.response is not None:
                try:
                    error_details = e.response.json()
                except requests.exceptions.JSONDecodeError:
                    error_details = e.response.text
                status_code = e.response.status_code
                reason = e.response.reason
            else:
                status_code = None
                reason = "Unknown reason"
            raise PoeNinjaRequestError(
                f"HTTP error occurred: {status_code} {reason}. Details: {error_details}",
                status_code=status_code,
            ) from e
        except requests.exceptions.RequestException as e:
            raise PoeNinjaRequestError(f"Request failed: {e}") from e

        try:
            data: JsonObject = response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise PoeNinjaAPIError(
                f"Failed to decode JSON response from {url}. Content: {response.text[:200]}..."
            ) from e
        return data

    def get_currency_overview(
        self, currency_type: CurrencyType
    ) -> CurrencyOverviewResponse:  # Changed to Enum
        """
        Fetches currency overview data for the initialized league.

        Args:
            currency_type (CurrencyType): The type of currency (e.g., CurrencyType.CURRENCY).

        Returns:
            CurrencyOverviewResponse: A structured object containing the currency overview data.
        """
        params: dict[str, Any] = {
            "league": self.league,
            "type": currency_type.value,  # Use Enum value
        }
        raw_json_response: JsonObject = self._request("currencyoverview", params=params)
        return parse_currency_overview_response(raw_json_response)

    def get_item_overview(
        self, item_type: ItemType
    ) -> ItemOverviewResponse:  # Changed to Enum
        """
        Fetches item overview data for the initialized league.

        Args:
            item_type (ItemType): The type of item (e.g., ItemType.UNIQUE_WEAPON).

        Returns:
            ItemOverviewResponse: A structured object containing the item overview data.
        """
        params: dict[str, Any] = {
            "league": self.league,
            "type": item_type.value,  # Use Enum value
        }
        raw_json_response: JsonObject = self._request("itemoverview", params=params)
        return parse_item_overview_response(raw_json_response)

    def find_currency(
        self, name: str, currency_type: CurrencyType
    ) -> Optional[CurrencyLine]:  # Changed to Enum
        """
        Finds a specific currency by its name within a given currency type.
        The search is case-insensitive.

        Args:
            name (str): The name of the currency to find (e.g., "Chaos Orb", "Divine Orb").
            currency_type (CurrencyType): The type of currency (e.g., CurrencyType.CURRENCY).

        Returns:
            Optional[CurrencyLine]: The found CurrencyLine object, or None if not found.
        """
        overview: CurrencyOverviewResponse = self.get_currency_overview(
            currency_type=currency_type
        )
        name_lower = name.lower()
        for currency_line in overview.lines:
            if currency_line.currencyTypeName.lower() == name_lower:
                return currency_line
        return None

    def find_item(
        self, name: str, item_type: ItemType
    ) -> Optional[ItemLine]:  # Changed to Enum
        """
        Finds a specific item by its name within a given item type.
        The search is case-insensitive.

        Args:
            name (str): The name of the item to find (e.g., "Headhunter", "Mageblood").
            item_type (ItemType): The type of item (e.g., ItemType.UNIQUE_ARMOUR for belts/shields).

        Returns:
            Optional[ItemLine]: The found ItemLine object, or None if not found.
        """
        overview: ItemOverviewResponse = self.get_item_overview(item_type=item_type)
        name_lower = name.lower()
        for item_line in overview.lines:
            if item_line.name.lower() == name_lower:
                return item_line
        return None

    def close(self) -> None:
        """Closes the underlying requests session."""
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
