# PoENinja Client

**PoENinja** is a Python client library for interacting with the public [poe.ninja API](https://poe.ninja/swagger/). It provides a simple, strictly-typed, and convenient interface to fetch various Path of Exile economy data for a specified league.

**Current Version:** 0.5.0

## Features

* **League-Specific Client:** Initialize the client for a specific Path of Exile league.
* **Typed API Responses:** Fetched data is parsed into Pydantic-like dataclasses for easy and type-safe access.
* **Enum-Driven Categories:** Uses Enums (`CurrencyType`, `ItemType`) for specifying data categories, reducing errors and improving code clarity.
* **Comprehensive Data Fetching:**
  * `get_currency_overview(currency_type: CurrencyType)`: Fetches bulk data for specified currency types (e.g., regular currency, fragments).
  * `get_item_overview(item_type: ItemType)`: Fetches bulk data for specified item types (e.g., unique weapons, skill gems).
* **Targeted Search:**
  * `find_currency(name: str, currency_type: CurrencyType)`: Quickly finds a specific currency item by name within its category.
  * `find_item(name: str, item_type: ItemType)`: Quickly finds a specific item by name within its category.
* **Session Management:** Uses `requests.Session` for efficient HTTP requests.
* **Custom Exceptions:** Clear error handling for API and request issues.
* **Context Manager Support:** Ensures resources like the HTTP session are properly managed.
* **Strictly Typed:** Designed for Python 3.12+ with full type hinting.

## Installation

Currently, the project is under development. To install it locally for development:

1.  Clone the repository:
    ```bash
    git clone https://your-repository-url/poe_ninja_project.git 
    # Replace with your actual repository URL
    cd poe_ninja_project
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
    CurrencyLine, # For type hinting specific results
    ItemLine      # For type hinting specific results
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

        # 3. Find a specific currency: Divine Orb
        print("\nSearching for 'Divine Orb'...")
        divine_orb: Optional[CurrencyLine] = client.find_currency(
            name="Divine Orb", 
            currency_type=CurrencyType.CURRENCY
        )
        if divine_orb:
            print(f"Found Divine Orb: {divine_orb.chaosEquivalent} Chaos")
            if divine_orb.receive:
                 # If Divine Orb is the "get_currency_id", 'value' is its price in the "pay_currency_id"
                 # If Chaos Orb is the "pay_currency_id", this 'value' is how many Chaos Orbs for 1 Divine Orb.
                print(f"  'receive.value' (e.g., Chaos per Divine if base is Chaos): {divine_orb.receive.value}")
        else:
            print("Divine Orb not found.")

        # 4. Find a specific item: The Squire (Unique Shield, falls under UniqueArmour)
        item_name_to_find = "The Squire"
        item_category = ItemType.UNIQUE_ARMOUR
        print(f"\nSearching for '{item_name_to_find}' in {item_category.value}...")
        the_squire: Optional[ItemLine] = client.find_item(
            name=item_name_to_find,
            item_type=item_category
        )
        if the_squire:
            print(f"Found The Squire: {the_squire.chaosValue} Chaos, Divine Value: {the_squire.divineValue}")
            print(f"  Icon: {the_squire.icon}")
        else:
            print(f"'{item_name_to_find}' not found in {item_category.value}.")
            
        # 5. Find a specific Skill Gem: Empower Support
        gem_name_to_find = "Empower Support" # Note: poe.ninja might list variants like "Empower Support (Level 4)"
        gem_category = ItemType.SKILL_GEM
        print(f"\nSearching for '{gem_name_to_find}' in {gem_category.value}...")
        # For items with variants (like gem levels/quality), the name needs to be exact or logic needs to handle partial matches.
        # The current find_item is an exact (case-insensitive) name match.
        empower_gem: Optional[ItemLine] = client.find_item(
            name=gem_name_to_find, # You might need to search for "Empower Support (Level 4)" for specific results
            item_type=gem_category
        )
        if empower_gem:
            print(f"Found {empower_gem.name}: Chaos: {empower_gem.chaosValue}, Level: {empower_gem.gemLevel}, Quality: {empower_gem.gemQuality}")
        else:
            print(f"'{gem_name_to_find}' (exact match) not found. Try specifying level/variant if applicable.")


except PoeNinjaRequestError as e:
    print(f"Request Error: {e} (Status Code: {e.status_code})")
except PoeNinjaAPIError as e:
    print(f"API Error: {e}")
except ValueError as e: # For issues like empty league string
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

## API Client Reference

### `PoENinja(league: str, user_agent: str = ...)`
Initializes the client for a specific `league`.

### Methods

* `get_currency_overview(currency_type: CurrencyType) -> CurrencyOverviewResponse`
* `get_item_overview(item_type: ItemType) -> ItemOverviewResponse`
* `find_currency(name: str, currency_type: CurrencyType) -> Optional[CurrencyLine]`
* `find_item(name: str, item_type: ItemType) -> Optional[ItemLine]`
* `close()`: Closes the session. Also called automatically when using a context manager.

### Enums

* `poe_ninja_client.CurrencyType`: Enum for currency categories.
    * Examples: `CurrencyType.CURRENCY`, `CurrencyType.FRAGMENT`, `CurrencyType.OIL`, etc.
* `poe_ninja_client.ItemType`: Enum for item categories.
    * Examples: `ItemType.UNIQUE_WEAPON`, `ItemType.UNIQUE_ARMOUR`, `ItemType.SKILL_GEM`, `ItemType.DIVINATION_CARD`, etc.

*(Note: The Enum lists in `enums.py` are not exhaustive and should be expanded to cover all types supported by the poe.ninja API.)*

### Data Models

The client returns data parsed into dataclasses (found in `poe_ninja_client.models`):
* `CurrencyOverviewResponse` (contains `list[CurrencyLine]`)
* `ItemOverviewResponse` (contains `list[ItemLine]`)
* `CurrencyLine`, `ItemLine`, `CurrencyTradeData`, `SparkLineData`, `ItemSparkLine`

Refer to `models.py` for the structure of these objects.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
(Further details on development setup, testing, and contribution guidelines can be added here).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
