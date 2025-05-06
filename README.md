# PoENinja Client

**PoENinja** is a Python client library for interacting with the public [poe.ninja API](https://poe.ninja/). It provides a simple, strictly-typed, and convenient interface to fetch various Path of Exile economy data for a specified league.

**Current Version:** 1.0.3

## Features

* **League-Specific Client:** Initialize the client for a specific Path of Exile league. All data fetching is league-dependent.
* **Typed API Responses:** Fetched data is parsed into dataclasses for easy and type-safe access.
* **Enum-Driven Categories:** Uses Enums (`CurrencyType`, `ItemType`) for specifying data categories, reducing errors and improving code clarity.
* **Comprehensive Data Fetching:**
    * `get_currency_overview(currency_type: CurrencyType)`: Fetches bulk data for specified currency types (e.g., regular currency, fragments).
    * `get_item_overview(item_type: ItemType)`: Fetches bulk data for specified item types (e.g., unique weapons, skill gems).
    * `get_currency_history(currency_type_for_history: CurrencyType, currency_id: int)`: Fetches historical price data for a specific currency.
    * `get_item_history(item_type_for_history: ItemType, item_id: int)`: Fetches historical price data for a specific item.
* **Convenience Lookups:**
    * `find_currency_line(name: str, currency_type: CurrencyType)`: Quickly finds a specific currency's overview data by name.
    * `find_item_line(name: str, item_type: ItemType)`: Quickly finds a specific item's overview data by name.
    * `get_currency_id_by_name(currency_name: str, overview_type: CurrencyType)`: Retrieves the numeric ID of a currency, needed for history lookups.
    * `get_item_id_by_name(item_name: str, item_type: ItemType)`: Retrieves the numeric ID of an item, needed for history lookups.
* **Session Management:** Uses `requests.Session` for efficient HTTP requests.
* **Custom Exceptions:** Clear error handling for API and request issues (`PoeNinjaRequestError`, `PoeNinjaAPIError`).
* **Context Manager Support:** Ensures resources like the HTTP session are properly managed.
* **Strictly Typed:** Designed for Python 3.12+ with full type hinting.

## Installation

Currently, the project is under development. To install it locally for development:

1.  Clone the repository:
    ```bash
    git clone https://github.com/infernumx/poe_ninja_client/poe_ninja_client.git 
    # Replace with your actual repository URL
    cd poe_ninja_client
    ```
2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install the package in editable mode:
    ```bash
    pip install -e .
    ```

Once packaged and uploaded to PyPI (e.g., as `poe-ninja-client`), it could be installed via:
```bash
pip install poe-ninja-client
```

## Requirements

* Python 3.12+
* `requests` (will be installed automatically if using pip)

## Basic Usage

```python
from poe_ninja_client import (
    PoENinja, 
    CurrencyType, 
    ItemType,
    PoeNinjaRequestError, 
    PoeNinjaAPIError,
    CurrencyLine, 
    ItemLine,
    HistoryResponse
)
from typing import Optional

# Replace with the current or desired Path of Exile league
# Ensure this league is active on poe.ninja
active_league = "Settlers" 

try:
    with PoENinja(league=active_league) as client:
        print(f"Client initialized for league: {client.league}")

        # 1. Get an overview of all standard currencies
        print(f"\nFetching all {CurrencyType.CURRENCY.value}...")
        currency_data = client.get_currency_overview(currency_type=CurrencyType.CURRENCY)
        print(f"Found {len(currency_data.lines)} currency entries.")
        if currency_data.lines:
            print(f"Example: {currency_data.lines[0].currencyTypeName} - Chaos Equivalent: {currency_data.lines[0].chaosEquivalent}")

        # 2. Get an overview of Unique Armours
        print(f"\nFetching all {ItemType.UNIQUE_ARMOUR.value}...")
        unique_armours = client.get_item_overview(item_type=ItemType.UNIQUE_ARMOUR)
        print(f"Found {len(unique_armours.lines)} unique armour entries.")
        if unique_armours.lines:
            first_armour = unique_armours.lines[0]
            print(f"Example: {first_armour.name} - Chaos Value: {first_armour.chaosValue}")

        # 3. Find a specific currency's overview data: Divine Orb
        print("\nSearching for 'Divine Orb' overview data...")
        divine_orb_line: Optional[CurrencyLine] = client.find_currency_line(
            name="Divine Orb", 
            currency_type=CurrencyType.CURRENCY
        )
        if divine_orb_line:
            print(f"Found Divine Orb in overview: {divine_orb_line.chaosEquivalent} Chaos")
        else:
            print("Divine Orb not found in overview.")

        # 4. Get history for Divine Orb
        currency_name_for_history = "Divine Orb"
        currency_type_for_id_lookup = CurrencyType.CURRENCY
        
        print(f"\nFetching numeric ID for '{currency_name_for_history}'...")
        divine_orb_numeric_id: Optional[int] = client.get_currency_id_by_name(
            currency_name_for_history, 
            overview_type=currency_type_for_id_lookup
        )

        if divine_orb_numeric_id is not None:
            print(f"Found numeric ID for {currency_name_for_history}: {divine_orb_numeric_id}")
            print(f"Fetching history for '{currency_name_for_history}' (ID: {divine_orb_numeric_id}, Type: {currency_type_for_id_lookup.value})...")
            divine_history: HistoryResponse = client.get_currency_history(
                currency_type_for_history=currency_type_for_id_lookup,
                currency_id=divine_orb_numeric_id
            )
            print(f"  Found {len(divine_history.data_points)} historical data points.")
            if divine_history.data_points:
                print(f"  Latest point: {divine_history.data_points[0].daysAgo} days ago, value: {divine_history.data_points[0].value}")
        else:
            print(f"Could not find numeric ID for '{currency_name_for_history}'.")
            
        # 5. Find a specific item's overview data: The Squire
        item_name_to_find = "The Squire"
        item_category_for_find = ItemType.UNIQUE_ARMOUR # Shields are under UniqueArmour
        print(f"\nSearching for '{item_name_to_find}' overview data in {item_category_for_find.value}...")
        the_squire_line: Optional[ItemLine] = client.find_item_line(
            name=item_name_to_find,
            item_type=item_category_for_find
        )
        if the_squire_line:
            print(f"Found The Squire in overview: {the_squire_line.chaosValue} Chaos")
            
            # 6. Get history for The Squire (using its numeric ID)
            print(f"\nFetching numeric ID for '{item_name_to_find}'...")
            squire_numeric_id: Optional[int] = client.get_item_id_by_name(
                item_name=item_name_to_find,
                item_type=item_category_for_find
            )
            if squire_numeric_id:
                print(f"Found numeric ID for {item_name_to_find}: {squire_numeric_id}")
                print(f"Fetching history for '{item_name_to_find}' (ID: {squire_numeric_id}, Type: {item_category_for_find.value})...")
                squire_history: HistoryResponse = client.get_item_history(
                    item_type_for_history=item_category_for_find,
                    item_id=squire_numeric_id
                )
                print(f"  Found {len(squire_history.data_points)} historical data points.")
                if squire_history.data_points:
                    print(f"  Latest point: {squire_history.data_points[0].daysAgo} days ago, value: {squire_history.data_points[0].value}")
            else:
                print(f"Could not find numeric ID for '{item_name_to_find}'.")
        else:
            print(f"'{item_name_to_find}' not found in {item_category_for_find.value} overview.")


except PoeNinjaRequestError as e:
    print(f"Request Error: {e} (Status Code: {e.status_code})")
except PoeNinjaAPIError as e:
    print(f"API Error: {e}")
except ValueError as e: 
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

## API Client Reference

### `PoENinja(league: str, user_agent: str = ...)`
Initializes the client for a specific `league`. The league name is mandatory.

### Methods

* **`get_currency_overview(currency_type: CurrencyType) -> CurrencyOverviewResponse`**
    Fetches an overview of currencies for the specified `currency_type` (e.g., `CurrencyType.CURRENCY`, `CurrencyType.FRAGMENT`).

* **`get_item_overview(item_type: ItemType) -> ItemOverviewResponse`**
    Fetches an overview of items for the specified `item_type` (e.g., `ItemType.UNIQUE_WEAPON`, `ItemType.DIVINATION_CARD`).

* **`find_currency_line(name: str, currency_type: CurrencyType) -> Optional[CurrencyLine]`**
    Searches the result of `get_currency_overview` for a currency by its exact name (case-insensitive). Returns the `CurrencyLine` object if found, else `None`.

* **`find_item_line(name: str, item_type: ItemType) -> Optional[ItemLine]`**
    Searches the result of `get_item_overview` for an item by its exact name (case-insensitive). Returns the `ItemLine` object if found, else `None`.

* **`get_currency_id_by_name(currency_name: str, overview_type: CurrencyType = CurrencyType.CURRENCY) -> Optional[int]`**
    Retrieves the numeric ID of a currency by its name. This ID is found in the `currencyDetails` part of a `CurrencyOverviewResponse` and is used as `currencyId` for the `get_currency_history` method.

* **`get_item_id_by_name(item_name: str, item_type: ItemType) -> Optional[int]`**
    Retrieves the numeric ID of an item by its name. This ID is found in the `ItemLine.id` field from an `ItemOverviewResponse` and is used as `itemId` for the `get_item_history` method.

* **`get_currency_history(currency_type_for_history: CurrencyType, currency_id: int) -> HistoryResponse`**
    Fetches 7-day price history for a specific currency.
    * `currency_type_for_history`: The `CurrencyType` Enum member (e.g., `CurrencyType.CURRENCY`).
    * `currency_id`: The numeric ID of the currency (obtained via `get_currency_id_by_name`).

* **`get_item_history(item_type_for_history: ItemType, item_id: int) -> HistoryResponse`**
    Fetches 7-day price history for a specific item.
    * `item_type_for_history`: The `ItemType` Enum member (e.g., `ItemType.UNIQUE_JEWEL`).
    * `item_id`: The numeric ID of the item (obtained via `get_item_id_by_name`).

* **`close()`**: Closes the underlying HTTP session. Called automatically when using the client as a context manager (`with PoENinja(...) as client:`).

### Enums

Located in `poe_ninja_client.enums`:

* **`CurrencyType(str, Enum)`**: Defines valid types for currency overviews and currency history (e.g., `CURRENCY`, `FRAGMENT`, `OIL`, `SCARAB`).
* **`ItemType(str, Enum)`**: Defines valid types for item overviews and item history (e.g., `UNIQUE_WEAPON`, `UNIQUE_ARMOUR`, `SKILL_GEM`, `DIVINATION_CARD`, `MAP`).

### Data Models

The client returns data parsed into dataclasses, defined in `poe_ninja_client.models`. Key models include:

* `CurrencyOverviewResponse`: Contains `lines: list[CurrencyLine]` and `currencyDetails: list[CurrencyDetail]`.
* `ItemOverviewResponse`: Contains `lines: list[ItemLine]`.
* `HistoryResponse`: Contains `data_points: list[PoeNinjaHistoryDataPoint]`.
* Individual line/detail models: `CurrencyLine`, `CurrencyDetail`, `ItemLine`, `PoeNinjaHistoryDataPoint`, `SparkLineData`, `CurrencyTradeData`, `ItemSparkLine`.

Refer to `models.py` for the detailed structure and fields of these objects.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
(Further details on development setup, testing, and contribution guidelines can be added here).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
